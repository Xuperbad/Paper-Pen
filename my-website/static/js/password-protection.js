// 简单的密码保护功能
(function() {
    // 密码配置
    const PASSWORDS = {
        'articles': '8768',
        'zhejiang': '8768',
        'fuxi': '8768',
        'zhenti': '8768',
        'notes': '8768'
    };

    // 需要保护的路径
    const PROTECTED_PATHS = ['/blog', '/zhejiang', '/fuxi', '/zhenti', '/notes'];

    // 检查是否已经通过验证
    function isAuthenticated(section) {
        return sessionStorage.getItem(`auth_${section}`) === 'true';
    }

    // 获取当前路径对应的section
    function getSectionFromPath(path) {
        if (path.startsWith('/blog')) return 'articles';
        if (path.startsWith('/zhejiang')) return 'zhejiang';
        if (path.startsWith('/fuxi')) return 'fuxi';
        if (path.startsWith('/zhenti')) return 'zhenti';
        if (path.startsWith('/notes')) return 'notes';
        return null;
    }

    // 检查当前页面是否需要密码保护
    function checkCurrentPage() {
        const currentPath = window.location.pathname;
        const section = getSectionFromPath(currentPath);
        
        if (section && !isAuthenticated(section)) {
            showPasswordModal(section);
        }
    }

    // 显示密码弹窗
    function showPasswordModal(section) {
        // 创建遮罩层
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;

        // 创建弹窗
        const modal = document.createElement('div');
        modal.style.cssText = `
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            min-width: 300px;
            text-align: center;
        `;

        modal.innerHTML = `
            <h3 style="margin-bottom: 20px; color: #333;">
                访问 ${section.toUpperCase()} 需要密码
            </h3>
            <input type="password" id="passwordInput" placeholder="请输入密码" style="
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 16px;
                box-sizing: border-box;
            " />
            <div id="errorMessage" style="color: red; margin-bottom: 15px; font-size: 14px; display: none;"></div>
            <div style="display: flex; gap: 10px; justify-content: center;">
                <button id="confirmBtn" style="
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                ">确认</button>
                <button id="cancelBtn" style="
                    padding: 10px 20px;
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                ">取消</button>
            </div>
        `;

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        const passwordInput = document.getElementById('passwordInput');
        const errorMessage = document.getElementById('errorMessage');
        const confirmBtn = document.getElementById('confirmBtn');
        const cancelBtn = document.getElementById('cancelBtn');

        // 自动聚焦到密码输入框
        passwordInput.focus();

        // 确认按钮点击事件
        function handleConfirm() {
            const password = passwordInput.value;
            if (password === PASSWORDS[section]) {
                // 密码正确，保存认证状态
                sessionStorage.setItem(`auth_${section}`, 'true');
                document.body.removeChild(overlay);
                // 重新加载页面以显示内容
                window.location.reload();
            } else {
                // 密码错误
                errorMessage.textContent = '密码错误，请重试';
                errorMessage.style.display = 'block';
                passwordInput.value = '';
                passwordInput.focus();
            }
        }

        // 取消按钮点击事件
        function handleCancel() {
            document.body.removeChild(overlay);
            // 跳转到首页
            window.location.href = '/';
        }

        confirmBtn.addEventListener('click', handleConfirm);
        cancelBtn.addEventListener('click', handleCancel);

        // 回车键确认
        passwordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleConfirm();
            }
        });
    }

    // 拦截导航链接点击
    function interceptNavigation() {
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a');
            if (!link) return;

            const href = link.getAttribute('href');
            if (!href) return;

            // 检查是否是受保护的路径
            const section = getSectionFromPath(href);
            if (section && !isAuthenticated(section)) {
                e.preventDefault();
                e.stopPropagation();
                showPasswordModal(section);
                return false;
            }
        }, true);
    }

    // 页面加载完成后执行
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            checkCurrentPage();
            interceptNavigation();
        });
    } else {
        checkCurrentPage();
        interceptNavigation();
    }
})();
