document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('img').forEach((image) => {
        image.loading = image.loading || 'lazy';
        image.decoding = image.decoding || 'async';
    });

    document.querySelectorAll('form').forEach((form) => {
        form.addEventListener('submit', () => {
            const submitter = form.querySelector('button[type="submit"]');
            if (submitter) {
                submitter.dataset.originalText = submitter.textContent;
                submitter.textContent = 'Working...';
                submitter.disabled = true;
            }
        });
    });
});
