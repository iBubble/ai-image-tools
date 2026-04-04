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
    let isUploaded = false;  // 区分上传图(低denoise保构图) vs 生成图(高denoise精修)
    // 从 localStorage 恢复历史记录
    let history = [];
    try { history = JSON.parse(localStorage.getItem('imgStudioHistory') || '[]'); } catch(e) { history = []; }

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
    
    // ── 随机生成 Prompt ──
    const $randomPromptBtn = document.getElementById('btn-random-prompt');
    if ($randomPromptBtn) {
        $randomPromptBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const origText = $randomPromptBtn.textContent;
            $randomPromptBtn.disabled = true;
            $randomPromptBtn.textContent = '⏳ 生成中...';
            $prompt.value = '正在呼叫 AI 构思极具创意的调教场景...';
            try {
                // 使用 Pollinations 的 Text LLM 接口，真正即时生成非预设组合的描述
                // 加入 seed 强制每次结果不同
                const seed = Math.floor(Math.random() * 9999999);
                // 改用标准的 POST JSON 格式请求，要求直接输出中文，便于微调
                const promptQuery = `You are a creative prompt engineer. Design a highly detailed, creative suspension shibari rope art scene with intricate knots, submissive helpless pose, and leather restraints for an image generator. Core tags: (full body shot:1.5), (showing entire body from head to toe:1.4), wide angle. Please translate all generated tags into Chinese keywords separated by commas. Return ONLY the Chinese tags. Do not explain. Example: (全身镜头:1.5), (从头到脚全身可见:1.4), 广角, 悬吊绳缚, 复杂的绳结. random_seed=${seed}`;
                
                const resp = await fetch('https://text.pollinations.ai/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        messages: [{ role: 'user', content: promptQuery }],
                        model: 'openai'
                    })
                });
                
                const txt = await resp.text();
                // 过滤掉系统的废话或者旧提示
                if (txt.includes("I'm sorry") || txt.includes("can't help") || txt.includes("IMPORTANT NOTICE")) {
                    throw new Error("Text API refused or returned notice");
                }
                $prompt.value = txt.trim().replace(/^"|"$/g, '');
            } catch (err) {
                // Fallback (若接口被屏蔽)
                const verbs = ["后折式猪蹄缚", "双膝跪伏于地", "悬吊于天花板", "M字开腿青蛙缚", "呈大字绑在X型木架上"];
                const bondage = ["重度日式麻绳捆绑", "极其紧绷的皮带束缚", "粗重的铁链", "全透明紧身乳胶衣"];
                const pick = arr => arr[Math.floor(Math.random()*arr.length)];
                $prompt.value = `(全身完整镜头:1.5), (画面展示从头到脚全部身体:1.4), 广角透视, ${pick(verbs)}, ${pick(bondage)}, 剧烈粗喘, 极致顺从卑微, 电影质感光影, 极高细节表现`;
            } finally {
                $randomPromptBtn.disabled = false;
                $randomPromptBtn.textContent = origText;
            }
        });
    }

    // ── 加载配置 ──
    fetch('./api/config').then(r => r.json()).then(cfg => {
        pollinationsKey = cfg.pollinations_key || '';
    }).catch(() => {});

    // ── 加载人物列表 ──
    fetch('./api/characters').then(r => r.json()).then(data => {
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
    function updateImageMeta(filename) {
        const meta = document.getElementById('image-meta');
        if (!meta) return;
        if (!filename) {
            meta.style.display = 'none';
            return;
        }
        // 解析文件名: poll_177_12345.jpg 或 refined_177_67890.png
        let parts = filename.split('.')[0].split('_');
        if (parts.length >= 3) {
            const seed = parts[parts.length - 1];
            const type = parts[0] === 'poll' ? 'Pollinations' : 'ComfyUI';
            meta.innerHTML = `🌟 引擎: <b>${type}</b> &nbsp;|&nbsp; 🎲 Seed: <b style="user-select:all; cursor:pointer;" title="双击复制">${seed}</b>`;
            meta.style.display = 'block';
        } else {
            meta.style.display = 'none';
        }
    }

    function showImage(url) {
        $image.src = url;
        $image.style.display = 'block';
        $placeholder.style.display = 'none';
        currentFilename = url.split('/').pop();
        updateImageMeta(currentFilename);
        // 启用推送/精修按钮
        document.getElementById('push-feishu').disabled = false;
        document.getElementById('push-lab').disabled = false;
        document.getElementById('refine-btn').disabled = false;
        document.getElementById('swap-face-btn').disabled = false;
        document.getElementById('download-btn').disabled = false;
        addHistory(url);
    }

    function addHistory(url) {
        // 去重
        history = history.filter(u => u !== url);
        history.unshift(url);
        if (history.length > 20) history = history.slice(0, 20);
        // 持久化到 localStorage
        try { localStorage.setItem('imgStudioHistory', JSON.stringify(history)); } catch(e) {}
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
                currentFilename = url.split('/').pop();
                updateImageMeta(currentFilename);
                document.getElementById('push-feishu').disabled = false;
                document.getElementById('push-lab').disabled = false;
                document.getElementById('refine-btn').disabled = false;
                document.getElementById('swap-face-btn').disabled = false;
                document.getElementById('download-btn').disabled = false;
            });
            $historyGrid.appendChild(img);
        });
    }
    // 页面加载时恢复历史
    if (history.length > 0) renderHistory();

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

        const resp = await fetch('./api/pollinations/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });
        const data = await resp.json();
        if (data.error) throw new Error(data.error);
        showImage(data.url);
        isUploaded = false;
        showStatus('success',
            `✅ ${keyLabel} | seed: ${data.seed} | model: ${data.model}`);
        // 自动精修
        if (document.getElementById('auto-refine').checked) {
            if (!character) {
                showStatus('error', '⚠️ 自动精修需要先选择人物预设');
            } else {
                setTimeout(() => refineImage(), 500);
            }
        }
        
        // 刷新额度
        fetchQuota();
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
        const resp = await fetch('./api/comfyui/generate', {
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
            endpoint === './api/push/feishu' ? 'push-feishu' : 'push-lab');
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
    window.pushToFeishu = () => _push('./api/push/feishu', '推送到飞书');
    window.pushToLab = () => _push('./api/push/lab', '推送到实验室');

    window.downloadImage = () => {
        if (!currentFilename) return;
        const a = document.createElement('a');
        a.href = `./api/image/${currentFilename}`;
        a.download = currentFilename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

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
            const resp = await fetch('./api/refine', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    filename: currentFilename,
                    character: character,
                    camera: cameraOverride || refineModel,
                    denoise: document.getElementById('cartoon-mode').checked ? 0.65 : 'auto',
                    scene_prompt: document.getElementById('prompt').value.trim(),
                    seed: -1
                })
            });
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            showImage(data.url);
            const typeLabel = data.img_type === 'cartoon' ? '🎨卡通' : '📷真人';
            showStatus('success',
                `✅ 精修完成 | ${typeLabel} | denoise: ${data.denoise} | model: ${data.model}`);
        } catch(e) {
            showStatus('error', `❌ 精修失败: ${e.message}`);
        } finally {
            btn.disabled = false;
            btn.textContent = origText;
        }
    };

    // ── 渐进式替换（换脸 / 换身 / 换人） ──
    const SWAP_LABELS = {
        face: {emoji: '🎭', name: '换头', time: '~30s'},
        body: {emoji: '💃', name: '换身', time: '~60s'},
        full: {emoji: '👤', name: '换人', time: '~90s'}
    };
    window.swapImage = async (mode) => {
        if (!currentFilename) { showStatus('error', '没有可处理的图片'); return; }
        if (!character) { showStatus('error', '请先选择人物预设'); return; }
        const info = SWAP_LABELS[mode];
        const btnId = `swap-${mode}-btn`;
        const btn = document.getElementById(btnId);
        const origText = btn.textContent;
        btn.disabled = true;
        btn.textContent = `⏳ ${info.name}中...`;
        showStatus('info', `${info.emoji} ${info.name}处理中... (${info.time})`);
        try {
            const resp = await fetch('./api/swap', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    filename: currentFilename,
                    character: character,
                    camera: refineModel,
                    mode: mode,
                    scene_prompt: document.getElementById('prompt').value.trim(),
                    seed: -1
                })
            });
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            showImage(data.url);
            showStatus('success', `✅ ${info.name}完成 | mode: ${mode} | denoise: ${data.denoise}`);
        } catch(e) {
            showStatus('error', `❌ ${info.name}失败: ${e.message}`);
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
            const up = await fetch('./api/upload', {
                method: 'POST', body: fd
            });
            const upData = await up.json();
            if (!upData.ok) throw new Error(upData.error);
            currentFilename = upData.filename;
            isUploaded = true;
            showImage(upData.url);
            showStatus('success',
                '✅ 上传成功，可点击精修按钮进行二次处理');
        } catch(e) {
            showStatus('error',
                '❌ 上传失败: ' + e.message);
        }
        input.value = '';
    };

    // ── 额度查询 ──
    async function fetchQuota() {
        const span = document.getElementById('quota-display');
        if (!span) return;
        try {
            const r = await fetch('./api/pollinations/quota');
            const d = await r.json();
            span.innerText = `⚡ Pollinations 剩余额度: ${d.balance.toFixed(3)} pt (约可生成 ${d.images_left} 张)`;
            span.style.color = d.images_left < 20 ? '#ff4d4f' : '#a0a0a0';
        } catch(e) {
            span.innerText = `⚡ Pollinations 剩余额度: 获取失败`;
        }
    }
    
    fetchQuota();
    setInterval(fetchQuota, 600000); // 10分钟

    // ── 放大查看逻辑 ──
    const $modal = document.getElementById('image-modal');
    const $modalImg = document.getElementById('modal-img');

    if ($image && $modal && $modalImg) {
        $image.style.cursor = 'zoom-in';
        $image.title = '点击放大查看';

        $image.addEventListener('click', () => {
            if ($image.src && $image.style.display !== 'none') {
                $modal.style.display = 'block';
                $modalImg.src = $image.src;
                // 防止页面背景滚动
                document.body.style.overflow = 'hidden';
            }
        });

        // 点击 Modal 任意区域关闭
        $modal.addEventListener('click', () => {
            $modal.style.display = 'none';
            document.body.style.overflow = '';
        });
    }

    // ── ComfyUI 状态与控制 ──
    const $comfyBtn = document.getElementById('comfyui-toggle-btn');
    const $comfySpinner = document.getElementById('comfyui-spinner');
    const $comfyText = document.getElementById('comfyui-toggle-text');
    let comfyStatus = 'checking'; // running, stopped, checking, starting, stopping

    async function checkComfyStatus() {
        if (comfyStatus === 'starting' || comfyStatus === 'stopping') return;
        try {
            const r = await fetch('./api/comfyui/status');
            const d = await r.json();
            updateComfyBtn(d.status);
        } catch(e) {
            updateComfyBtn('stopped');
        }
    }

    function updateComfyBtn(status) {
        comfyStatus = status;
        if (!$comfyBtn) return;
        if (status === 'running') {
            $comfyBtn.style.background = 'rgba(34,197,94,0.15)';
            $comfyBtn.style.color = '#86efac';
            $comfyText.textContent = '🖥️ ComfyUI 已启动 (点击可停止)';
            $comfySpinner.style.display = 'none';
        } else if (status === 'stopped') {
            $comfyBtn.style.background = 'rgba(239,68,68,0.15)';
            $comfyBtn.style.color = '#fca5a5';
            $comfyText.textContent = '🔌 ComfyUI 未启动 (点击唤醒)';
            $comfySpinner.style.display = 'none';
        } else if (status === 'starting') {
            $comfyBtn.style.background = 'rgba(59,130,246,0.15)';
            $comfyBtn.style.color = '#93c5fd';
            $comfyText.textContent = '⏳ 正在加载模型... (~30秒)';
            $comfySpinner.style.display = 'inline-block';
        } else if (status === 'stopping') {
            $comfyBtn.style.background = 'rgba(245,158,11,0.15)';
            $comfyBtn.style.color = '#fcd34d';
            $comfyText.textContent = '🛑 正在停止...';
            $comfySpinner.style.display = 'inline-block';
        }
    }

    if ($comfyBtn) {
        $comfyBtn.addEventListener('click', async () => {
            if (comfyStatus === 'running') {
                updateComfyBtn('stopping');
                await fetch('./api/comfyui/stop', { method: 'POST' });
                setTimeout(checkComfyStatus, 2000);
            } else if (comfyStatus === 'stopped') {
                updateComfyBtn('starting');
                await fetch('./api/comfyui/start', { method: 'POST' });
                
                let checkCount = 0;
                const startInterval = setInterval(async () => {
                    checkCount++;
                    try {
                        const r = await fetch('./api/comfyui/status');
                        const d = await r.json();
                        if (d.status === 'running') {
                            updateComfyBtn('running');
                            clearInterval(startInterval);
                        }
                    } catch(e) {}
                    if (checkCount > 30) { // 60秒超时
                        clearInterval(startInterval);
                        checkComfyStatus();
                    }
                }, 2000);
            }
        });
        checkComfyStatus();
        setInterval(checkComfyStatus, 10000); 
    }
})();
