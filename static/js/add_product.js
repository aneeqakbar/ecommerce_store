
function previewFiles(event) {
    var img_cont = document.getElementById('image_upload_cont');
    var files = event.target.files;
    var img_upload = document.getElementsByClassName('preview_main')[0].cloneNode(true);

    function readAndPreview(file,index) {
        if (index >= 12) {
            return
        }

        // Make sure `file.name` matches our extensions criteria
        //   if ( /\.(jpe?g|png|gif)$/i.test(file.name) ) {
        if (file.name.split('.').pop() == 'jpeg' || 'png') {
            var reader = new FileReader();
            reader.addEventListener("load", function () {

                let div = create_Preview_Div()

                var image = new Image();
                image.height = 100;
                image.title = file.name;
                image.src = this.result; // the result is the reader.readAsDataURL(file); return value

                div.append(image);
                img_cont.prepend(div);
                img_cont.lastElementChild.remove()

                images = document.querySelectorAll('.preview > img')
                img_upload_exists  = images[images.length-1].parentElement.nextElementSibling;
                if (img_upload_exists === null) {
                    img_upload.classList.add('no_display')
                    img_cont.append(img_upload);
                }
            }, false);

            reader.readAsDataURL(file);
        }
    }

    function create_Preview_Div() {
        let div = document.createElement('div')
        div.classList.add('preview')

        let close = document.createElement('div')
        close.classList.add('preview_close')
        close.setAttribute('onclick', 'removePreview(this)')
        close.innerText = 'X'

        let preview_cover = document.createElement('div')
        preview_cover.classList.add('preview_cover', 'no_display')
        preview_cover.innerText = 'Cover'
        div.append(preview_cover);
        div.append(close);
        return div
    }
    function manageCover() {
        let preview_covers = document.querySelectorAll('.preview_cover')
        preview_covers.forEach(element => {
            element.classList.add('no_display')
        })
        preview_covers[0].classList.remove('no_display')
    };

    if (files) {
        for (let i = 0; i < files.length; i++) {
            readAndPreview(files[i],i)
        }
        setTimeout(() => {
            manageCover()
        }, 200);
        // [].forEach.call(files, readAndPreview)
    }
}

function removePreview(element) {
    var img_cont = document.getElementById('image_upload_cont');
    element.parentElement.remove()

    var preview = document.querySelectorAll('.preview');
    if (preview[preview.length - 1].classList.contains('no_display')) {
        preview[preview.length - 1].classList.remove('no_display')
    }
    else {
        let icon = document.createElement('i')
        icon.classList.add('fa', 'fa-camera')

        let div = document.createElement('div')
        div.classList.add('preview', 'preview_fade')
        div.append(icon)

        img_cont.append(div)
    }
}
