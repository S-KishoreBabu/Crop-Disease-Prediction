const dropArea = document.getElementById('drop-area');

dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropArea.classList.add('hover');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('hover');
});

dropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    dropArea.classList.remove('hover');

    const files = event.dataTransfer.files;
    handleFiles(files);
});

function handleFiles(files) {
    for (const file of files) {
        if (!file.type.startsWith('image/')) {
            continue;
        }
        
        const img = document.createElement('img');
        img.classList.add('obj');
        img.file = file;
        document.getElementById('gallery').appendChild(img);

        const reader = new FileReader();
        reader.onload = (function (aImg) {
            return function (e) {
                aImg.src = e.target.result;
            };
        })(img);
        reader.readAsDataURL(file);
    }
}
