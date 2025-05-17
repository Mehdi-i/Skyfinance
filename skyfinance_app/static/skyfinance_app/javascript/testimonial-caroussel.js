
const next = document.querySelector('.next-testimonial');
const previous = document.querySelector('.previous-testimonial');
const slides = document.querySelectorAll('.slides');

let index = 0;
display(index);

function display(index) {
     slides.forEach((slide) => {
        slide.style.display = 'none';
    });
    slides[index].style.display = 'flex';
}

function nextSlide() {
    index++;
    if (index > slides.length - 1) {
        index = 0
    }

    display(index);
}

function previousSlide() {
    index--;
    if (index < 0) {
        index = slides.length - 1
    }
    display(index);
}

next.addEventListener('click', nextSlide);
previous.addEventListener('click', previousSlide);

