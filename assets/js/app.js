{const e=()=>{document.documentElement.style.setProperty("--body-scroll-width",window.innerWidth-document.documentElement.clientWidth+"px")};window.addEventListener("resize",e),e()}{const e=()=>{setDarkMode(!isDarkMode());const e=isDarkMode();localStorage.setItem("darkMode",e?"1":"0")},t=e=>{e.checked=isDarkMode()};document.querySelectorAll("[data-darkmode-toggle] input, [data-darkmode-switch] input").forEach((n=>{n.addEventListener("change",e),t(n)}))}document.querySelectorAll(".uc-horizontal-scroll").forEach((e=>{e.addEventListener("wheel",(t=>{t.preventDefault(),e.scrollBy({left:t.deltaY,behavior:"smooth"})}))})),document.addEventListener("DOMContentLoaded",(()=>{const e=document.querySelector("[data-uc-backtotop]");if(!e)return;e.addEventListener("click",(e=>{e.preventDefault(),window.scrollTo({top:0,behavior:"smooth"})}));let t=0;window.addEventListener("scroll",(()=>{const n=document.body.getBoundingClientRect().top;e.parentNode.classList.toggle("uc-active",n<=t),t=n}))})),document.addEventListener("DOMContentLoaded",(function(){let e=[].slice.call(document.querySelectorAll("video.video-lazyload"));function t(e){let t=e.querySelector("source");t.src=t.dataset.src,e.load(),e.muted=!0,"visible"===document.visibilityState?e.play():document.addEventListener("visibilitychange",(function t(){"visible"===document.visibilityState&&(e.play(),document.removeEventListener("visibilitychange",t))}))}if("IntersectionObserver"in window){let n=new IntersectionObserver((function(e,o){e.forEach((function(e){if(e.isIntersecting){let o=e.target;t(o),n.unobserve(o)}}))}));e.forEach((function(e){n.observe(e),e.getBoundingClientRect().top<window.innerHeight&&e.getBoundingClientRect().bottom>0&&(t(e),n.unobserve(e))}))}else e.forEach((function(e){t(e)}))}));
const currentUrl = window.location.href;
document.getElementById('page-url').value = `${currentUrl}`

function minimizeNumber(num) {
    const absNum = Math.abs(num);
    
    if (absNum >= 1000000) {
        const millions = absNum / 1000000;
        if (millions > 1.2) {
            return '+1.2 M';
        }
        return (millions % 1 === 0) ? millions + ' M' : millions.toFixed(1) + ' M';
    }
    
    if (absNum >= 1000) {
        const thousands = absNum / 1000;
        return (thousands % 1 === 0) ? thousands + ' B' : thousands.toFixed(1) + ' B';
    }
    
    return num.toString();
}

function processMinimizeNumbers() {
    const elements = document.querySelectorAll('.minimizeNumber');
    
    elements.forEach(element => {
        const textContent = element.textContent.trim();
        const number = parseFloat(textContent.replace(/[^\d.-]/g, ''));
        
        // Geçerli bir sayı ise işle
        if (!isNaN(number)) {
            element.textContent = minimizeNumber(number);
        }
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processMinimizeNumbers);
} else {
    processMinimizeNumbers();
}

const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1) { 
                if (node.matches && node.matches('.minimizeNumber')) {
                    const number = parseFloat(node.textContent.trim().replace(/[^\d.-]/g, ''));
                    if (!isNaN(number)) {
                        node.textContent = minimizeNumber(number);
                    }
                }
                const childElements = node.querySelectorAll && node.querySelectorAll('.minimizeNumber');
                if (childElements) {
                    childElements.forEach(element => {
                        const number = parseFloat(element.textContent.trim().replace(/[^\d.-]/g, ''));
                        if (!isNaN(number)) {
                            element.textContent = minimizeNumber(number);
                        }
                    });
                }
            }
        });
    });
});

// Tarih kısaltma fonksiyonu
function minimizeDate(dateStr, isMobile) {
    // Tarih formatını kontrol et (gün.ay.yıl)
    const datePattern = /(\d{1,2})\.(\d{1,2})\.(\d{4})/;
    const match = dateStr.match(datePattern);
    
    if (!match) return dateStr; // Geçersiz format ise olduğu gibi bırak
    
    const day = match[1];
    const month = match[2];
    const year = match[3];
    
    if (isMobile) {
        // Mobilde yılı son 2 hanesi olarak göster
        const shortYear = year.slice(-2);
        return `${day}.${month}.${shortYear}`;
    }
    
    return dateStr; // Desktop'ta olduğu gibi bırak
}

// Ekran genişliğini kontrol et
function isMobileView() {
    return window.innerWidth < 768;
}

// minimizeDate class'ına sahip tüm elementleri bul ve işle
function processMinimizeDates() {
    const elements = document.querySelectorAll('.minimizeDate');
    const isMobile = isMobileView();
    
    elements.forEach(element => {
        const originalText = element.getAttribute('data-original-date') || element.textContent.trim();
        
        // İlk çalışmada orijinal tarihi kaydet
        if (!element.hasAttribute('data-original-date')) {
            element.setAttribute('data-original-date', originalText);
        }
        
        const minimizedDate = minimizeDate(originalText, isMobile);
        element.textContent = minimizedDate;
    });
}

// Sayfa yüklendiğinde çalıştır
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', processMinimizeDates);
} else {
    processMinimizeDates();
}

// Ekran boyutu değiştiğinde yeniden işle
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(processMinimizeDates, 100);
});

// Dinamik olarak eklenen elementler için MutationObserver kullan
const dateObserver = new MutationObserver(mutations => {
    let shouldProcess = false;
    
    mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1) { // Element node
                // Yeni eklenen node .minimizeDate ise
                if (node.matches && node.matches('.minimizeDate')) {
                    shouldProcess = true;
                }
                // Alt elementlerde .minimizeDate var mı kontrol et
                const childElements = node.querySelectorAll && node.querySelectorAll('.minimizeDate');
                if (childElements && childElements.length > 0) {
                    shouldProcess = true;
                }
            }
        });
    });
    
    if (shouldProcess) {
        processMinimizeDates();
    }
});