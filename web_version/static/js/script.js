let mediaRecorder;
let audioChunks = [];

function startRecording() {
    audioChunks = []; // 重置 audioChunks

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                // 測試播放錄製的音訊
                playRecordedAudio();
                sendAudioToServer();
            };

            mediaRecorder.onerror = (err) => {
                console.error("錄音錯誤:", err);
            };

            mediaRecorder.start();
            console.log("錄音開始，MediaRecorder 狀態:", mediaRecorder.state);
        })
        .catch(err => {
            console.error("錄音設備錯誤:", err);
        });
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        console.log("錄音結束，MediaRecorder 狀態:", mediaRecorder.state);
    } else {
        console.warn("MediaRecorder 目前不在錄音狀態");
    }
}

function playRecordedAudio() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    console.log("播放錄製的音訊");
}

function sendAudioToServer() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
    const formData = new FormData();
    formData.append('audio', audioBlob, 'voirec.mp3');

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("伺服器回應錯誤: " + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        let arr = data.text.split('@@');
        document.getElementById('transcription').textContent ="您描述的心情是："+ arr[0];
        document.getElementById('recommend').textContent ="AI建議："+arr[1];
        document.getElementById('movie').innerHTML ="<video  autoplay width='640' height='480' src="+arr[2]+">";
    })
    .catch(err => {
        console.error("音訊上傳或轉錄錯誤:", err);
    });
}