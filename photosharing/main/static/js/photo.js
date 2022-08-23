const form = document.querySelector('.post-form');
const mediaURL = window.location.origin + '/media/';
const effectSelect = document.getElementById('id_effect');

console.log(effectSelect);

let photoID = null;
let photoSaved = false;
effectSelect.addEventListener('change', (event) => {
    photoSaved = false;

    const description = document.getElementById('id_description');
    const location = document.getElementById('id_location');
    const imageChooser = document.getElementById('file-ip-1');
    const effect = event.target.value;

    if (imageChooser.files[0] && effect) {
        if (photoID) {
            $.ajax({
                type: 'DELETE',
                url: window.location.origin + '/photo_delete/' + photoID,
                headers: {'X-CSRFToken': Cookies.get('csrftoken')},
                success: function(response){
                    console.log(response);
                },
                error: function(error){
                    console.log(error)
                },
                cache: false,
                contentType: false,
                processData: false,
            });
        }

        const fd = new FormData();
        fd.append('description', description.value);
        fd.append('location', location.value);
        fd.append('effect', effect);
        fd.append('photo_path', imageChooser.files[0]);

        $.ajax({
            type: 'POST',
            url: window.location.origin + '/upload_post/',
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response){
                const data = JSON.parse(response.data)
                console.log(data)

                photoID = data[0].pk;

                const preview = document.getElementById("file-ip-1-preview");
                preview.src = mediaURL + data[0].fields.photo_path;
            },
            error: function(error){
                console.log(error)
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    }
});


form.addEventListener('submit', (event) => {
    event.preventDefault();
    photoSaved = true;

    const description = document.getElementById('id_description');
    const location = document.getElementById('id_location');
    const effect = document.getElementById('id_effect');
    const imageChooser = document.getElementById('file-ip-1');

    if (!photoID) {
        const fd = new FormData();
        fd.append('description', description.value);
        fd.append('location', location.value);
        fd.append('effect', effect.value);
        fd.append('photo_path', imageChooser.files[0]);

         $.ajax({
            type: 'POST',
            url: window.location.origin + '/add_photo/',
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response){
                 window.location.href = window.location.origin + '/home';
            },
            error: function(error){
                console.log(error)
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    } else {
        const fd = new FormData();
        fd.append('description', description.value);
        fd.append('location', location.value);

         $.ajax({
            type: 'POST',
            url: window.location.origin + '/photo_update/' + photoID,
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response){
                 window.location.href = window.location.origin + '/home';
            },
            error: function(error){
                console.log(error)
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    }
});

function showPreview(event){
  if(event.target.files.length > 0){
    var src = URL.createObjectURL(event.target.files[0]);
    var preview = document.getElementById("file-ip-1-preview");
    preview.src = src;
    preview.style.display = "block";
    }
}