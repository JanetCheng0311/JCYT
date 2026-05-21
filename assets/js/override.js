
function removeFramerBadge() {
    const badge = document.querySelector('div[id^="__framer-badge-container"]');
    if (badge) badge.remove();
}

function enforceMultimedia() {
    const targets = ["Communication design", "Communication Design", "Communication designer", "Communication Designer"];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while (node = walker.nextNode()) {
        targets.forEach(t => {
            if (node.nodeValue.includes(t)) {
                node.nodeValue = node.nodeValue.replace(t, "Multimedia designer");
            }
        });
    }
}

function updateResumeImages() {
    // Exact mapping for each page container class
    const mapping = [
        { cls: 'framer-1muv3pg', src: 'latest_resume/CV_cyt_2026_01.jpg' },
        { cls: 'framer-nixoin',  src: 'latest_resume/CV_cyt_2026_02.jpg' },
        { cls: 'framer-124nu4y', src: 'latest_resume/CV_cyt_2026_03.jpg' }
    ];

    mapping.forEach(m => {
        document.querySelectorAll('.' + m.cls + ' img').forEach(img => {
            if (img.getAttribute('src') !== m.src) {
                img.src = m.src;
            }
            if (img.srcset) {
                img.srcset = '';
                img.removeAttribute('srcset');
            }
        });
    });

    // Ensure Page 3 is visible
    document.querySelectorAll('.framer-124nu4y').forEach(el => {
        el.style.setProperty('opacity', '1', 'important');
        el.style.setProperty('visibility', 'visible', 'important');
    });
}


function fixLayoutGaps() {
    // Force the main resume container to be top/left 0
    document.querySelectorAll('.framer-1glz78b').forEach(el => {
        el.style.setProperty('top', '0', 'important');
        el.style.setProperty('left', '0', 'important');
    });

    // Also look for common grey square container patterns
    // Often they have a specific background color or are at the top edge
    document.querySelectorAll('div').forEach(el => {
        const style = window.getComputedStyle(el);
        if (style.position === 'absolute' && 
            (parseInt(style.top) < 10) && 
            (parseInt(style.left) < 100)) {
            // If it's very close to the top-left, snap it
            if (parseInt(style.left) > 0 && parseInt(style.left) < 50) {
                 el.style.setProperty('left', '0', 'important');
            }
             if (parseInt(style.top) > 0 && parseInt(style.top) < 50) {
                 el.style.setProperty('top', '0', 'important');
            }
        }
    });
}

function snapTopRightGrey() {
    // Target the thin grey bar that Framer often places near the top-right
    document.querySelectorAll('.framer-sf0z71, .framer-8tn6n9').forEach(el => {
        try {
            el.style.setProperty('position', 'absolute', 'important');
            el.style.setProperty('top', '0', 'important');
            el.style.setProperty('left', '0', 'important');
            el.style.setProperty('right', '0', 'important');
            el.style.setProperty('width', '100%', 'important');
            el.style.setProperty('max-width', '100%', 'important');
            el.style.setProperty('box-sizing', 'border-box', 'important');
        } catch (e) {
            // ignore
        }
    });
}

const observer = new MutationObserver(() => {
    removeFramerBadge();
    enforceMultimedia();
    updateResumeImages();
    fixLayoutGaps();
    snapTopRightGrey();
});

observer.observe(document.body, { childList: true, subtree: true });

// Initial run
removeFramerBadge();
enforceMultimedia();
updateResumeImages();
fixLayoutGaps();
snapTopRightGrey();
