var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(element) {
    parent = element.parentNode
    grandparent = parent.parentNode
    for (let i = 0; i < grandparent.children.length; i++) {
        if (grandparent.children[i].children[0].alt === element.alt) {
            // console.log('matched!',i)
            return showSlides(slideIndex = i + 1)
        }
    }
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("demo");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].classList.add("active");
    var numbertext = document.getElementById("numbertext");
    numbertext.innerText = `${slideIndex} / ${slides.length}`
}


