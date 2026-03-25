/* Image Studio — 前端逻辑 */
(function() {
    'use strict';

    // ── 状态 ──
    let engine = 'pollinations';
    let model = 'zimage';
    let pollinationsKey = '';
    let currentFilename = '';
    let character = '';
    let refineModel = 'moody';
    const history = [];

    // ── DOM ──
    const $prompt = document.getElementById('prompt');
    const $negative = document.getElementById('negative');
    const $seed = document.getElementById('seed');
    const $size = document.getElementById('size');
    const $safe = document.getElementById('safe-mode');
    const $genBtn = document.getElementById('generate-btn');
    const $btnText = document.querySelector('.btn-text');
    const $btnLoad = document.querySelector('.btn-loading');
    const $status = document.getElementById('status');
    const $image = document.getElementById('result-image');
    const $placeholder = document.getElementById('placeholder');
    const $historyGrid = document.getElementById('history-grid');

    // ── 按钮组切换 ──
    function setupGroup(id, callback) {
        const group = document.getElementById(id);
        group.querySelectorAll('.btn-option').forEach(btn => {
            btn.addEventListener('click', () => {
                group.querySelectorAll('.btn-option').forEach(
                    b => b.classList.remove('active'));
                btn.classList.add('active');
                callback(btn.dataset.value);
            });
        });
    }

    setupGroup('engine-group', val => {
        engine = val;
        const mg = document.getElementById('model-group');
        mg.innerHTML = '';
        const models = val === 'pollinations'
            ? [['zimage','ZImage'], ['flux','Flux']]
            : [['moody','Moody'], ['pornmaster','Pornmaster']];
        models.forEach(([v, l], i) => {
            const b = document.createElement('button');
            b.className = 'btn-option' + (i===0?' active':'');
            b.dataset.value = v;
            b.textContent = l;
            b.addEventListener('click', () => {
                mg.querySelectorAll('.btn-option').forEach(
                    x => x.classList.remove('active'));
                b.classList.add('active');
                model = v;
            });
            mg.appendChild(b);
        });
        model = models[0][0];
    });

    setupGroup('model-group', val => { model = val; });

    // ── 加载配置 ──
    fetch('/api/config').then(r => r.json()).then(cfg => {
        pollinationsKey = cfg.pollinations_key || '';
    }).catch(() => {});

    // ── 加载人物列表 ──
    fetch('/api/characters').then(r => r.json()).then(data => {
        const cg = document.getElementById('character-group');
        (data.characters || []).forEach(ch => {
            const b = document.createElement('button');
            b.className = 'btn-option';
            b.dataset.value = ch.key;
            b.textContent = ch.label;
            b.addEventListener('click', () => {
                cg.querySelectorAll('.btn-option').forEach(
                    x => x.classList.remove('active'));
                b.classList.add('active');
                character = ch.key;
            });
            cg.appendChild(b);
        });
        const noneBtn = cg.querySelector('[data-value=""]');
        if (noneBtn) noneBtn.addEventListener('click', () => {
            cg.querySelectorAll('.btn-option').forEach(
                x => x.classList.remove('active'));
            noneBtn.classList.add('active');
            character = '';
        });
    }).catch(() => {});

    // ── 显示状态 ──
    function showStatus(type, msg) {
        $status.className = 'status ' + type;
        $status.textContent = msg;
        $status.style.display = 'block';
    }
    function hideStatus() { $status.style.display = 'none'; }

    // ── 显示图片 ──
    function showImage(url) {
        $image.src = url;
        $image.style.display = 'block';
        $placeholder.style.display = 'none';
        currentFilename = url.split('/').pop();
        // 启用推送/精修按钮
        document.getElementById('push-feishu').disabled = false;
        document.getElementById('push-lab').disabled = false;
        document.getElementById('refine-btn').disabled = false;
        addHistory(url);
    }

    function addHistory(url) {
        history.unshift(url);
        if (history.length > 20) history.pop();
        renderHistory();
    }

    function renderHistory() {
        $historyGrid.innerHTML = '';
        history.forEach(url => {
            const img = document.createElement('img');
            img.src = url;
            img.addEventListener('click', () => {
                $image.src = url;
                $image.style.display = 'block';
                $placeholder.style.display = 'none';
            });
            $historyGrid.appendChild(img);
        });
    }

    // ── 生成 ──
    function setLoading(on) {
        $genBtn.disabled = on;
        $btnText.style.display = on ? 'none' : 'inline';
        $btnLoad.style.display = on ? 'inline' : 'none';
    }

    $genBtn.addEventListener('click', async () => {
        const prompt = $prompt.value.trim();
        if (!prompt) { showStatus('error', '请输入提示词'); return; }
        hideStatus();
        setLoading(true);

        try {
            if (engine === 'pollinations') {
                await generatePollinations(prompt);
            } else {
                await generateComfyUI(prompt);
            }
        } catch (e) {
            showStatus('error', '生成失败: ' + e.message);
        } finally {
            setLoading(false);
        }
    });

    async function generatePollinations(prompt) {
        const [w, h] = ($size.value || '1024x1024').split('x');
        const seed = $seed.value || Math.floor(Math.random()*2e9);
        const useKey = document.getElementById('use-api-key').checked;
        const keyLabel = useKey ? '有Key' : '无Key';

        showStatus('info', `⚡ Pollinations (${keyLabel}) 生成中...`);

        const body = {
            prompt,
            model,
            width: parseInt(w),
            height: parseInt(h),
            seed: parseInt(seed),
            safe: $safe.checked ? 'true' : 'false',
            use_key: useKey,
            enhance: document.getElementById('enhance-mode').checked,
            character: character
        };
        const neg = ($negative.value || '').trim();
        if (neg) body.negative_prompt = neg;

        const resp = await fetch('/api/pollinations/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });
        const data = await resp.json();
        if (data.error) throw new Error(data.error);
        showImage(data.url);
        showStatus('success',
            `✅ ${keyLabel} | seed: ${data.seed} | model: ${data.model}`);
    }

    async function generateComfyUI(prompt) {
        showStatus('info', '🖥️ ComfyUI 生成中... (约 100 秒)');
        const body = {
            prompt,
            negative_prompt: ($negative.value || '').trim(),
            model,
            seed: $seed.value ? parseInt($seed.value) : -1,
            character: character
        };
        const resp = await fetch('/api/comfyui/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });
        const data = await resp.json();
        if (data.error) throw new Error(data.error);
        showImage(data.url);
        showStatus('success',
            `✅ 生成完成 | seed: ${data.seed} | model: ${data.model}`);
    }

    // ── 推送功能（全局暴露） ──
    async function _push(endpoint, label) {
        if (!currentFilename) {
            showStatus('error', '没有可推送的图片');
            return;
        }
        const btn = document.getElementById(
            endpoint === '/api/push/feishu' ? 'push-feishu' : 'push-lab');
        const origText = btn.textContent;
        btn.disabled = true;
        btn.textContent = '⏳ 推送中...';
        try {
            const resp = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({filename: currentFilename})
            });
            const data = await resp.json();
            if (data.ok) {
                showStatus('success', `✅ ${label}成功`);
            } else {
                showStatus('error', `❌ ${label}失败: ${data.error}`);
            }
        } catch(e) {
            showStatus('error', `❌ ${label}失败: ${e.message}`);
        } finally {
            btn.disabled = false;
            btn.textContent = origText;
        }
    }
    window.pushToFeishu = () => _push('/api/push/feishu', '推送到飞书');
    window.pushToLab = () => _push('/api/push/lab', '推送到实验室');

    window.setRefineModel = (val) => {
        refineModel = val;
        document.getElementById('rm-moody').classList.toggle('active', val === 'moody');
        document.getElementById('rm-porn').classList.toggle('active', val === 'pornmaster');
    };

    window.refineImage = async (cameraOverride) => {
        if (!currentFilename) {
            showStatus('error', '没有可精修的图片');
            return;
        }
        if (!character) {
            showStatus('error', '请先选择人物预设再精修');
            return;
        }
        const btn = document.getElementById('refine-btn');
        const origText = btn.textContent;
        btn.disabled = true;
        btn.textContent = '⏳ 精修中 (~120s)...';
        showStatus('info', '🔄 ComfyUI img2img 精修中... (约 120 秒)');
        try {
            const resp = await fetch('/api/refine', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    filename: currentFilename,
                    character: character,
                    camera: cameraOverride || refineModel,
                    denoise: 0.7,
                    scene_prompt: $prompt.value.trim(),
                    seed: -1
                })
            });
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            showImage(data.url);
            showStatus('success',
                `✅ 精修完成 | denoise: ${data.denoise} | model: ${data.model}`);
        } catch(e) {
            showStatus('error', `❌ 精修失败: ${e.message}`);
        } finally {
            btn.disabled = false;
            btn.textContent = origText;
        }
    };

    window.uploadImage = async (input) => {
        const file = input.files[0];
        if (!file) return;
        showStatus('info', '⬆️ 上传中...');
        const fd = new FormData();
        fd.append('file', file);
        try {
            const up = await fetch('/api/upload', {
                method: 'POST', body: fd
            });
            const upData = await up.json();
            if (!upData.ok) throw new Error(upData.error);
            currentFilename = upData.filename;
            showImage(upData.url);
            showStatus('success',
                '✅ 上传成功，可点击精修按钮进行二次处理');
        } catch(e) {
            showStatus('error',
                '❌ 上传失败: ' + e.message);
        }
        input.value = '';
    };
})();
