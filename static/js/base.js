let avatar_cont = document.getElementById('nav__avatar__cont');
let avatar_drop = document.getElementById('nav__avatar__drop');
let arrow_icon = document.querySelector('#nav__avatar__cont > i');
let avatar_text = document.querySelectorAll('.no_profile_pic > span');

let username = JSON.parse(document.getElementById('req_username'));
username = username?.textContent

let notification_cont = document.getElementById('notification_cont');
let notification_drop = document.getElementById('notification_drop');

let hamburger = document.getElementById('nav__right__collapse__btn');
let nav__right__collapse__body = document.getElementById('nav__right__collapse__body');

window.addEventListener("load",() => {
    avatar_text_changer(avatar_text,username);
})


hamburger.addEventListener('click',()=>{
    toggle_drop(nav__right__collapse__body)
})


function avatar_text_changer(avatar_text,username) {
    avatar_text.forEach(element => {
        element.innerText = username[0].toUpperCase();
    });
}

avatar_cont.onfocus = (event)=>{
    toggle_drop(avatar_drop,arrow_icon)
}
avatar_cont.onblur = (event)=>{
    toggle_drop(avatar_drop,arrow_icon)
}

notification_cont.onfocus = (event)=>{
    toggle_drop(notification_drop)
}
notification_cont.onblur = (event)=>{
    toggle_drop(notification_drop)
}


function toggle_drop(element,arrow_icon=null) {
    if (arrow_icon != null) {
        if (arrow_icon.classList.contains("fa-rotate-180") && element.style.display === 'none') {
            arrow_icon.classList.remove('fa-rotate-180');
            element.style.display = 'block'
        }else{
            setTimeout(() => {
                arrow_icon.classList.add('fa-rotate-180');
                element.style.display = 'none'
            }, 200);
        }
    }
    else{
        if (element.style.display === 'none') {
            element.style.display = 'block'
        }else{
            setTimeout(()=>{
                element.style.display = 'none'
            },100)
        }
    }
}

let notifications_id = []

function notification_callback(data) {
    let notification_drop_options = document.getElementById('notification_drop_options')
    for (var i=0; i < data.unread_list.length; i++) {
        msg = data.unread_list[i];

        if (notifications_id.filter(id => id == msg.id).length == 0) {
            let div = createNotificationElement(msg)
            notification_drop_options.appendChild(div)
            notifications_id.push(msg.id)
        }
    }
}

function createNotificationElement(msg){
    let date_from_now = moment(msg.timestamp).fromNow();
    let div = document.createElement('div')
    let p = document.createElement('p')
    let small = document.createElement('small')
    div.classList.add('nav__drop__details__option__cont')
    p.textContent = msg.description
    small.textContent = date_from_now
    p.appendChild(small)
    div.appendChild(p)
    return div
}
