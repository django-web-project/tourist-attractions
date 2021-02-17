document.querySelectorAll(".drop-zone__input").forEach(inputElement => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    // 클릭 시, 이미지 업로드
    dropZoneElement.addEventListener("click", e => {
       inputElement.click();
    });

    inputElement.addEventListener("change", e => {
       if(inputElement.files.length) {
           updateThumbnail(dropZoneElement, inputElement.files[0]);
       }
    });

    dropZoneElement.addEventListener("dragover", e => {
        e.preventDefault();
        dropZoneElement.classList.add("drop-zone--over");
    });
    ["dragleave", "dragend"].forEach(type => {
       dropZoneElement.addEventListener(type, e => {
          dropZoneElement.classList.remove("drop-zone--over");
       });
    });

    dropZoneElement.addEventListener("drop", e => {
        e.preventDefault();
        // console.log(e.dataTransfer.files);

        // 파일 들어옴
        if(e.dataTransfer.files.length) {
            inputElement.files = e.dataTransfer.files;
            updateThumbnail(dropZoneElement, e.dataTransfer.files[0])
        }

        dropZoneElement.classList.remove("drop-zone--over");
    });
});


function updateThumbnail(dropzoneElement, file) {
    // console.log(dropzoneElement);
    // console.log(file);
    let thumbnailElement = dropzoneElement.querySelector(".drop-zone__thumb");

    // prompt 삭제
    if(dropzoneElement.querySelector(".drop-zone__prompt")) {
        dropzoneElement.querySelector(".drop-zone__prompt").remove();
    }

    // 썸네일이 없을 경우, 생성
    if(!thumbnailElement) {
        thumbnailElement = document.createElement("div");
        thumbnailElement.classList.add("drop-zone__thumb");
        dropzoneElement.appendChild(thumbnailElement);
    }

    thumbnailElement.dataset.label = file.name;

    // 썸네일 show
    if(file.type.startsWith('image/')) {
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = () => {
            thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
        }
    } else {
        thumbnailElement.style.backgroundImage = null;
    }
}