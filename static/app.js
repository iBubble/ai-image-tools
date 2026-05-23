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
    // 从 localStorage 恢复历史记录并严密过滤脏数据
    let history = [];
    try { 
        const raw = localStorage.getItem('imgStudioHistory');
        history = JSON.parse(raw || '[]'); 
        if (!Array.isArray(history)) history = [];
        history = history.filter(x => x && (typeof x === 'string' || x.url));
    } catch(e) { 
        history = []; 
    }
    let currentBalance = null;

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
                if (typeof updateQuotaDisplay === 'function') updateQuotaDisplay();
            });
            mg.appendChild(b);
        });
        model = models[0][0];
        if (typeof updateQuotaDisplay === 'function') updateQuotaDisplay();
    });

    setupGroup('model-group', val => { 
        model = val; 
        if (typeof updateQuotaDisplay === 'function') updateQuotaDisplay();
    });
    
    // ── 随机生成 Prompt（调用后端多维度组合引擎） ──
    const $randomPromptBtn = document.getElementById('btn-random-prompt');
    if ($randomPromptBtn) {
        $randomPromptBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const origText = $randomPromptBtn.textContent;
            $randomPromptBtn.disabled = true;
            $randomPromptBtn.textContent = '🎲 组合中...';
            try {
                // 获取主题选择（如果存在下拉菜单）
                const $themeSelect = document.getElementById('prompt-theme');
                const theme = $themeSelect ? $themeSelect.value : '';
                const url = theme
                    ? `./api/random-prompt?theme=${encodeURIComponent(theme)}`
                    : './api/random-prompt';
                const resp = await fetch(url);
                const data = await resp.json();
                if (data.prompt) {
                    $prompt.value = data.prompt;
                    // 在控制台输出维度详情（方便调试）
                    if (data.dimensions) {
                        console.log('🎲 随机提示词维度:', data.dimensions);
                    }
                } else {
                    throw new Error('后端返回为空');
                }
            } catch (err) {
                console.error('随机提示词生成失败:', err);
                $prompt.value = '⚠️ 生成失败，请重试';
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

    function showImage(url, metaOverride = {}) {
        console.log('🔮 [ImageStudio] showImage 被调用, url:', url, 'metaOverride:', metaOverride);
        $image.src = url;
        $image.style.display = 'block';
        $placeholder.style.display = 'none';
        currentFilename = url.split('/').pop();
        updateImageMeta(currentFilename);
        
        // 启用推送/精修按钮
        const btns = ['push-feishu', 'push-lab', 'refine-btn', 'swap-face-btn', 'download-btn'];
        btns.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.disabled = false;
        });

        // 构造完整的历史元数据
        let parts = currentFilename.split('.')[0].split('_');
        let parsedSeed = -1;
        if (parts.length >= 3) {
            let s = parseInt(parts[parts.length - 1]);
            if (!isNaN(s)) parsedSeed = s;
        }

        const historyItem = {
            url: url,
            prompt: metaOverride.prompt || $prompt.value.trim(),
            negative_prompt: metaOverride.negative_prompt || $negative.value.trim(),
            seed: metaOverride.seed !== undefined ? metaOverride.seed : (parsedSeed !== -1 ? parsedSeed : ($seed.value ? parseInt($seed.value) : -1)),
            character: metaOverride.character || character,
            engine: metaOverride.engine || engine,
            model: metaOverride.model || model,
            timestamp: Date.now()
        };

        console.log('🔮 [ImageStudio] 生成的历史元数据 historyItem:', historyItem);
        addHistory(historyItem);
    }

    function addHistory(item) {
        if (!item) return;
        const itemUrl = typeof item === 'string' ? item : item.url;
        if (!itemUrl) return;

        console.log('🔮 [ImageStudio] addHistory 被调用, 历史项 URL:', itemUrl);
        const itemFilename = itemUrl.split('/').pop();

        // 统一利用文件名进行安全且绝对的去重
        history = history.filter(x => {
            if (!x) return false;
            const u = typeof x === 'string' ? x : x.url;
            if (!u) return false;
            return u.split('/').pop() !== itemFilename;
        });

        history.unshift(item);
        if (history.length > 20) history = history.slice(0, 20);

        // 持久化到 localStorage
        try { 
            localStorage.setItem('imgStudioHistory', JSON.stringify(history)); 
            console.log('💾 [ImageStudio] 成功持久化历史记录至 localStorage');
        } catch(e) {
            console.error('❌ [ImageStudio] 写入 localStorage 失败:', e);
        }
        renderHistory();
    }

    function renderHistory() {
        console.log('🔮 [ImageStudio] 开始渲染历史缩略图, 当前列表大小:', history.length);
        $historyGrid.innerHTML = '';
        history.forEach(item => {
            if (!item) return;
            const isStr = typeof item === 'string';
            const url = isStr ? item : item.url;
            if (!url) return;
            const img = document.createElement('img');
            img.src = url;
            img.addEventListener('click', () => {
                try {
                    console.log('🔮 [ImageStudio] 点击历史缩略图切换:', url);
                    $image.src = url;
                    $image.style.display = 'block';
                    $placeholder.style.display = 'none';
                    currentFilename = url.split('/').pop();
                    updateImageMeta(currentFilename);

                    // 激活所有功能按钮
                    const btns = ['push-feishu', 'push-lab', 'refine-btn', 'swap-face-btn', 'download-btn'];
                    btns.forEach(id => {
                        const el = document.getElementById(id);
                        if (el) el.disabled = false;
                    });

                    // 完美回填状态与参数还原
                    if (!isStr) {
                        if (item.prompt !== undefined) $prompt.value = item.prompt;
                        if (item.negative_prompt !== undefined) $negative.value = item.negative_prompt;
                        
                        // 回填 Seed
                        if (item.seed !== undefined && item.seed !== -1) {
                            $seed.value = item.seed;
                        } else {
                            $seed.value = '';
                        }

                        // 魔法回填人物预设
                        if (item.character !== undefined) {
                            const cg = document.getElementById('character-group');
                            if (cg) {
                                const charBtn = cg.querySelector(`[data-value="${item.character}"]`);
                                if (charBtn) charBtn.click();
                            }
                        }

                        // 魔法回填引擎和模型
                        if (item.engine !== undefined && item.model !== undefined) {
                            const eg = document.getElementById('engine-group');
                            if (eg) {
                                const engineBtn = eg.querySelector(`[data-value="${item.engine}"]`);
                                if (engineBtn) engineBtn.click();
                            }
                            setTimeout(() => {
                                const mg = document.getElementById('model-group');
                                if (mg) {
                                    const modelBtn = mg.querySelector(`[data-value="${item.model}"]`);
                                    if (modelBtn) modelBtn.click();
                                }
                            }, 50);
                        }
                    } else {
                        // 如果是旧的单纯字符串 URL，我们只从文件名尝试恢复 Seed
                        let parts = currentFilename.split('.')[0].split('_');
                        if (parts.length >= 3) {
                            const parsedSeed = parseInt(parts[parts.length - 1]);
                            if (!isNaN(parsedSeed)) {
                                $seed.value = parsedSeed;
                            }
                        }
                    }
                } catch (err) {
                    console.error('❌ [ImageStudio] 切换历史记录大图时发生异常:', err);
                }
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
        showImage(data.url, {
            prompt: prompt,
            negative_prompt: ($negative.value || '').trim(),
            seed: data.seed,
            character: character,
            engine: 'comfyui',
            model: data.model || model
        });
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
            showImage(data.url, {
                prompt: document.getElementById('prompt').value.trim(),
                negative_prompt: document.getElementById('negative').value.trim(),
                seed: data.seed,
                character: data.character || character,
                engine: 'comfyui',
                model: data.model || refineModel
            });
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
            showImage(data.url, {
                prompt: document.getElementById('prompt').value.trim(),
                negative_prompt: document.getElementById('negative').value.trim(),
                seed: data.seed,
                character: character,
                engine: 'comfyui',
                model: refineModel
            });
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
            showImage(upData.url, {
                prompt: '',
                negative_prompt: '',
                seed: -1,
                character: '',
                engine: 'upload',
                model: ''
            });
            showStatus('success',
                '✅ 上传成功，可点击精修按钮进行二次处理');
        } catch(e) {
            showStatus('error',
                '❌ 上传失败: ' + e.message);
        }
        input.value = '';
    };

    // ── 额度查询 ──
    let fetchSuccess = true;

    function updateQuotaDisplay() {
        const span = document.getElementById('quota-display');
        if (!span || currentBalance === null) return;
        
        if (!fetchSuccess) {
            span.innerText = `⚡ Pollinations 剩余额度: 未知 (API Key 权限受限)`;
            span.style.color = '#ffa940';
            return;
        }

        let costPerImage = 0.002; // 统一按照 0.002 pt/张计算
        if (model === 'flux') {
            costPerImage = 0.002; 
        } else if (model === 'zimage') {
            costPerImage = 0.002;
        }
        
        let images_left = Math.floor(currentBalance / costPerImage);
        span.innerText = `⚡ Pollinations 剩余额度: ${currentBalance.toFixed(3)} pt (约可生成 ${images_left} 张)`;
        span.style.color = images_left < 20 ? '#ff4d4f' : '#a0a0a0';
    }

    async function fetchQuota() {
        const span = document.getElementById('quota-display');
        if (!span) return;
        try {
            const r = await fetch('./api/pollinations/quota');
            const d = await r.json();
            currentBalance = d.balance;
            fetchSuccess = d.fetch_success;
            updateQuotaDisplay();
        } catch(e) {
            span.innerText = `⚡ Pollinations 剩余额度: 获取失败`;
            fetchSuccess = false;
        }
    }
    
    fetchQuota();
    setInterval(fetchQuota, 600000); // 10分钟

    // ── 放大查看逻辑 ──
    const $modal = document.getElementById('image-modal');
    const $modalImg = document.getElementById('modal-img');
    const $modalPrev = document.getElementById('modal-prev');
    const $modalNext = document.getElementById('modal-next');
    const $modalDebug = document.getElementById('modal-debug');
    let currentModalIndex = -1;

    // 提取纯文件名（安全过滤协议、主机名、相对路径、Query参数及哈希的干扰）
    function getCleanFilename(url) {
        if (!url) return '';
        try {
            const decoded = decodeURIComponent(url);
            const pathOnly = decoded.split('?')[0].split('#')[0];
            return pathOnly.split('/').pop();
        } catch (e) {
            return url.split('/').pop() || '';
        }
    }

    function updateModalNavButtons() {
        if ($modalDebug) {
            $modalDebug.style.display = 'none'; // 调试完成，正式环境隐藏以确保视觉高级感
        }
        if (!$modalPrev || !$modalNext) return;
        if (currentModalIndex === -1 || history.length <= 1) {
            $modalPrev.style.display = 'none';
            $modalNext.style.display = 'none';
        } else {
            // 历史记录视觉排布：左侧为新 (index小)，右侧为旧 (index大)
            // 左按钮（Prev）向左走 -> 指向更新的图，即 index 减小，当前 index 必须 > 0 才能点
            $modalPrev.style.display = currentModalIndex > 0 ? 'block' : 'none';
            // 右按钮（Next）向右走 -> 指向更旧的图，即 index 增大，当前 index 必须 < history.length - 1 才能点
            $modalNext.style.display = currentModalIndex < history.length - 1 ? 'block' : 'none';
        }
    }

    if ($image && $modal && $modalImg) {
        $image.style.cursor = 'zoom-in';
        $image.title = '点击放大查看';

        $image.addEventListener('click', () => {
            if ($image.src && $image.style.display !== 'none') {
                $modal.style.display = 'block';
                $modalImg.src = $image.src;
                // 防止页面背景滚动
                document.body.style.overflow = 'hidden';

                // 查找当前图片在 history 中的索引
                const currentFilename = getCleanFilename($image.src);
                currentModalIndex = history.findIndex(item => {
                    const u = typeof item === 'string' ? item : item.url;
                    return u && getCleanFilename(u) === currentFilename;
                });
                updateModalNavButtons();
            }
        });

        // 点击 Modal 任意区域关闭（排除导航按钮）
        $modal.addEventListener('click', (e) => {
            if (e.target.id === 'modal-prev' || e.target.id === 'modal-next') {
                return;
            }
            $modal.style.display = 'none';
            document.body.style.overflow = '';
        });

        if ($modalPrev) {
            $modalPrev.addEventListener('click', (e) => {
                e.stopPropagation();
                if (currentModalIndex > 0) { // 向左切换 (更近/更新生成的图，索引递减)
                    currentModalIndex--;
                    const item = history[currentModalIndex];
                    const url = typeof item === 'string' ? item : item.url;
                    $modalImg.src = url;
                    updateModalNavButtons();
                    // 同步背后的主图
                    const imgs = $historyGrid.querySelectorAll('img');
                    if (imgs[currentModalIndex]) imgs[currentModalIndex].click();
                }
            });
        }

        if ($modalNext) {
            $modalNext.addEventListener('click', (e) => {
                e.stopPropagation();
                if (currentModalIndex < history.length - 1) { // 向右切换 (更早/更旧生成的图，索引递增)
                    currentModalIndex++;
                    const item = history[currentModalIndex];
                    const url = typeof item === 'string' ? item : item.url;
                    $modalImg.src = url;
                    updateModalNavButtons();
                    // 同步背后的主图
                    const imgs = $historyGrid.querySelectorAll('img');
                    if (imgs[currentModalIndex]) imgs[currentModalIndex].click();
                }
            });
        }

        // ── 键盘快捷键支持 (Esc关闭，左右方向键导航) ──
        document.addEventListener('keydown', (e) => {
            if ($modal && $modal.style.display === 'block') {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    if ($modalPrev && currentModalIndex > 0) {
                        $modalPrev.click();
                    }
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    if ($modalNext && currentModalIndex < history.length - 1) {
                        $modalNext.click();
                    }
                } else if (e.key === 'Escape') {
                    e.preventDefault();
                    $modal.style.display = 'none';
                    document.body.style.overflow = '';
                }
            }
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
