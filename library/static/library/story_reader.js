(() => {
    const reader = document.querySelector('[data-page-reader]');
    if (!reader) return;

    const book = reader.querySelector('[data-page-flip]');
    const pages = Array.from(book.querySelectorAll('.book-page'));
    const backButton = reader.querySelector('[data-page-back]');
    const nextButton = reader.querySelector('[data-page-next]');
    const counter = reader.querySelector('[data-page-counter]');
    const soundButton = reader.querySelector('[data-sound-toggle]');
    const sound = reader.querySelector('[data-page-turn-sound]');
    const errorMessage = reader.querySelector('[data-reader-error]');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const contentPageCount = pages.length;
    let soundEnabledByInteraction = false;
    let muted = false;

    if (!window.St || typeof window.St.PageFlip !== 'function') {
        errorMessage.hidden = false;
        throw new Error('The local StPageFlip browser library did not load.');
    }

    if (pages.length === 1) {
        const blankPage = document.createElement('article');
        blankPage.className = 'book-page book-page-blank';
        blankPage.setAttribute('aria-hidden', 'true');
        book.appendChild(blankPage);
    }

    const pageFlip = new window.St.PageFlip(book, {
        width: 480,
        height: 640,
        size: 'stretch',
        minWidth: 280,
        maxWidth: 560,
        minHeight: 380,
        maxHeight: 800,
        drawShadow: true,
        maxShadowOpacity: 0.4,
        showCover: false,
        usePortrait: true,
        autoSize: true,
        flippingTime: reducedMotion.matches ? 1 : 900,
        mobileScrollSupport: false,
        swipeDistance: 40,
        clickEventForward: true,
        disableFlipByClick: false,
    });

    const updateControls = () => {
        const currentIndex = pageFlip.getCurrentPageIndex();
        const spreadSize = pageFlip.getOrientation() === 'landscape' ? 2 : 1;
        const visiblePage = Math.min(currentIndex + spreadSize, contentPageCount);
        counter.textContent = `Page ${visiblePage} of ${contentPageCount}`;
        backButton.disabled = currentIndex <= 0;
        nextButton.disabled = visiblePage >= contentPageCount;
    };

    const playPageTurnSound = () => {
        if (!soundEnabledByInteraction || muted) return;
        sound.pause();
        sound.currentTime = 0;
        sound.volume = 0.2;
        sound.play().catch((error) => {
            console.warn('Could not play the page-turn recording.', error);
        });
    };

    reader.addEventListener('pointerdown', () => {
        soundEnabledByInteraction = true;
    }, { once: true });
    reader.addEventListener('click', () => {
        soundEnabledByInteraction = true;
    }, { once: true });

    pageFlip.on('flip', () => {
        updateControls();
        playPageTurnSound();
    });
    pageFlip.on('changeOrientation', updateControls);
    pageFlip.loadFromHTML(book.querySelectorAll('.book-page'));

    backButton.addEventListener('click', () => pageFlip.flipPrev('bottom'));
    nextButton.addEventListener('click', () => pageFlip.flipNext('bottom'));
    soundButton.addEventListener('click', () => {
        muted = !muted;
        soundButton.setAttribute('aria-pressed', String(muted));
        soundButton.textContent = muted ? 'Unmute sound' : 'Mute sound';
    });

    document.addEventListener('keydown', (event) => {
        if (event.target instanceof Element
            && event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
            event.preventDefault();
            pageFlip.flipNext('bottom');
        } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
            event.preventDefault();
            pageFlip.flipPrev('bottom');
        }
    });

    updateControls();
})();
