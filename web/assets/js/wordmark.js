//   PlayAlong
//   Copyright (c) 2026 Fooxygen.
//   With BaseTUT.
//   Licensed under the MIT License.

(() => {
    const section = document.querySelector(".wordmark-section");
    const canvas = document.getElementById("wordmark-canvas");

    if (!section || !canvas) {
        return;
    }

    const ctx = canvas.getContext("2d", { alpha: false });
    const textCanvas = document.createElement("canvas");
    const textCtx = textCanvas.getContext("2d", { alpha: true });

    const TEXT = "PLAYALONG";
    const BACKGROUND = "#f472b6";
    const FOREGROUND = "#f7f4ff";
    const MOVING_WINDOW_MS = 90;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let width = 1;
    let height = 1;
    let dpr = 1;
    let fontSize = 1;
    let lastWidth = 0;
    let lastHeight = 0;
    let fontReady = false;

    let pointerX = -100000;
    let pointerY = -100000;
    let velocityX = 0;
    let velocityY = 0;
    let lastClientX = null;
    let lastClientY = null;
    let pointerActive = false;

    let intensity = 0;
    let lastMoveAt = 0;
    let frame = 0;
    let resizeTimer = 0;

    function paintText() {
        textCtx.clearRect(0, 0, width, height);
        textCtx.fillStyle = FOREGROUND;
        textCtx.textAlign = "center";
        textCtx.textBaseline = "middle";

        let size = height * 0.72;
        const maxWidth = width * 0.84;
        textCtx.font = `900 ${size}px "Keinann Maru POP", "Maple Mono", sans-serif`;

        const measured = textCtx.measureText(TEXT).width;
        if (measured > maxWidth) {
            size *= maxWidth / measured;
            textCtx.font = `900 ${size}px "Keinann Maru POP", "Maple Mono", sans-serif`;
        }

        fontSize = size;
        textCtx.fillText(TEXT, width / 2, height / 2);
    }

    function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function drawWarpedArea(rows, cols, radius) {
        const cellWidth = width / cols;
        const cellHeight = height / rows;

        const minCol = Math.max(0, Math.floor((pointerX - radius) / cellWidth));
        const maxCol = Math.min(cols - 1, Math.floor((pointerX + radius) / cellWidth));
        const minRow = Math.max(0, Math.floor((pointerY - radius) / cellHeight));
        const maxRow = Math.min(rows - 1, Math.floor((pointerY + radius) / cellHeight));

        const left = Math.floor(minCol * cellWidth);
        const top = Math.floor(minRow * cellHeight);
        const right = Math.floor((maxCol + 1) * cellWidth);
        const bottom = Math.floor((maxRow + 1) * cellHeight);

        ctx.fillStyle = BACKGROUND;
        ctx.fillRect(left, top, right - left, bottom - top);

        const maxShiftX = cellWidth;
        const maxShiftY = cellHeight;

        for (let row = minRow; row <= maxRow; row++) {
            const y = Math.floor(row * cellHeight);
            const yEnd = Math.floor((row + 1) * cellHeight);
            const blockHeight = Math.max(1, yEnd - y);

            for (let col = minCol; col <= maxCol; col++) {
                const x = Math.floor(col * cellWidth);
                const xEnd = Math.floor((col + 1) * cellWidth);
                const blockWidth = Math.max(1, xEnd - x);

                const centerX = x + blockWidth / 2;
                const centerY = y + blockHeight / 2;
                const distance = Math.hypot(centerX - pointerX, centerY - pointerY);
                const falloff = Math.max(0, 1 - distance / radius);

                let dx = 0;
                let dy = 0;

                if (falloff > 0 && intensity > 0.005) {
                    dx =
                        clamp(velocityX * dpr * 1.4, -maxShiftX, maxShiftX) *
                        falloff *
                        intensity;
                    dy =
                        clamp(velocityY * dpr * 1.4, -maxShiftY, maxShiftY) *
                        falloff *
                        intensity;
                }

                ctx.drawImage(
                    textCanvas,
                    x,
                    y,
                    blockWidth,
                    blockHeight,
                    x + Math.round(dx),
                    y + Math.round(dy),
                    blockWidth,
                    blockHeight
                );
            }
        }
    }

    function draw(now) {
        const moving = pointerActive && now - lastMoveAt < MOVING_WINDOW_MS;
        const target = moving ? 1 : 0;

        intensity += (target - intensity) * (reduceMotion ? 1 : 0.18);
        velocityX *= 0.82;
        velocityY *= 0.82;

        ctx.fillStyle = BACKGROUND;
        ctx.fillRect(0, 0, width, height);
        ctx.drawImage(textCanvas, 0, 0);

        if (!reduceMotion && intensity > 0.005) {
            const rows = 8;
            const cols = 16;
            const radius = Math.min(width, height) * 0.6;
            drawWarpedArea(rows, cols, radius);
        }

        if (!reduceMotion && (moving || intensity > 0.01)) {
            frame = requestAnimationFrame(draw);
        } else {
            frame = 0;
        }
    }

    function start() {
        if (!frame) {
            frame = requestAnimationFrame(draw);
        }
    }

    function resize() {
        if (!fontReady) {
            return;
        }

        const rect = section.getBoundingClientRect();
        if (Math.abs(rect.width - lastWidth) < 0.5 && Math.abs(rect.height - lastHeight) < 0.5) {
            return;
        }
        lastWidth = rect.width;
        lastHeight = rect.height;

        dpr = Math.min(window.devicePixelRatio || 1, 1.25);
        width = Math.min(2560, Math.max(1, Math.round(rect.width * dpr)));
        height = Math.min(720, Math.max(1, Math.round(rect.height * dpr)));

        canvas.width = width;
        canvas.height = height;
        textCanvas.width = width;
        textCanvas.height = height;

        paintText();

        if (frame) {
            cancelAnimationFrame(frame);
            frame = 0;
        }
        draw(performance.now());
    }

    function movePointer(clientX, clientY) {
        const rect = section.getBoundingClientRect();
        pointerX = (clientX - rect.left) * dpr;
        pointerY = (clientY - rect.top) * dpr;

        if (lastClientX !== null && lastClientY !== null) {
            velocityX = velocityX * 0.6 + (clientX - lastClientX) * 0.4;
            velocityY = velocityY * 0.6 + (clientY - lastClientY) * 0.4;
        }

        lastClientX = clientX;
        lastClientY = clientY;
        lastMoveAt = performance.now();
        pointerActive = true;
        start();
    }

    section.addEventListener("pointermove", (event) => {
        movePointer(event.clientX, event.clientY);
    });

    section.addEventListener("pointerleave", () => {
        pointerActive = false;
        velocityX = 0;
        velocityY = 0;
        lastClientX = null;
        lastClientY = null;
        start();
    });

    section.addEventListener("pointercancel", () => {
        pointerActive = false;
        velocityX = 0;
        velocityY = 0;
        lastClientX = null;
        lastClientY = null;
        start();
    });

    section.addEventListener(
        "wheel",
        (event) => {
            const rect = section.getBoundingClientRect();
            pointerX = (event.clientX - rect.left) * dpr;
            pointerY = (event.clientY - rect.top) * dpr;
            velocityX += event.deltaX * 0.08;
            velocityY += event.deltaY * 0.08;
            lastMoveAt = performance.now();
            pointerActive = true;
            start();
        },
        { passive: true }
    );

    window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(resize, 150);
    });

    document.fonts
        .load('900 90px "Keinann Maru POP"')
        .then(() => {
            fontReady = true;
            resize();
        })
        .catch(() => {
            fontReady = true;
            resize();
        });
})();
