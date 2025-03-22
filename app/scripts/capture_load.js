function processResponse(data) {
    console.log(data)
}

function uploadFile() {
    fileInput.click()
}

function uploadCamera() {
    const video = dquery("#camera")
    const canvas = dquery("#canvas")
    const context = canvas.getContext("2d")
    
    const videoWidth = video.videoWidth;
    const videoHeight = video.videoHeight;

    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;

    const videoAspectRatio = videoWidth / videoHeight;
    const canvasAspectRatio = canvasWidth / canvasHeight;

    let drawWidth, drawHeight, offsetX = 0, offsetY = 0;

    if (videoAspectRatio > canvasAspectRatio) {
        drawWidth = videoWidth;
        drawHeight = videoWidth / canvasAspectRatio;
        offsetY = (drawHeight - videoHeight) / 2 * -1;
    } else {
        drawHeight = videoHeight;
        drawWidth = videoHeight * canvasAspectRatio;
        offsetX = (drawWidth - videoWidth) / 2 * -1;
    }
    context.drawImage(video, offsetX, offsetY, drawWidth, drawHeight, 0, 0, canvasWidth, canvasHeight);
    const base64Image = canvas.toDataURL("image/jpeg")

    fetch("http://localhost:8002/api/process", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ image: base64Image })
    })
        .then(response => response.json())
        .then(response => {
            processResponse(response)
        })
}

var fileInput
window.onload = function() {
    fileInput = dquery("#fileUpload")
    const video = dquery('#camera');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error("Error accessing the camera: ", error);
        });
    }

    fileInput.onchange = function(e) {
        const file = fileInput.files[0];
        let formData = new FormData();
        formData.append('image', file);

        fetch("http://localhost:8002/api/process", {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(response => {
                processResponse(response)
            })
    }
}