// Copy link in the Send_message place
function copyUrl() {
    const locationUrl = document.getElementById('locationUrl')
    locationUrl.select()
    locationUrl.setSelectionRange(0, 99999)
    document.execCommand("copy")
    alert("Copied")
}

// Share secrete link to whatsapp in View secrete link page
function SendToWhatsapp() {
    const locationUrl = document.getElementById('locationUrl').value;
    url = "https://wa.me/?text=" + locationUrl;
    window.location.href = url
    console.log(url)
}



// Copy URL in profile page 
function copyLink() {
    unique_link = document.getElementById('unique-link')
    unique_link.select();
    unique_link.setSelectionRange(0, 99999);
    document.execCommand("copy")
    alert("Copied")
}


// Generate QR Image

const qrImage = document.getElementById('qrImage');
const qrLink = document.getElementById('unique-link');

function generateQr() {
    const qrCodeUrl = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + qrLink.value;
    qrImage.src = qrCodeUrl;
}

function downloadQr() {
    const qrCodeUrl = qrImage.src;

    fetch(qrCodeUrl)
        .then(response => response.blob()) // Convert the response to a Blob
        .then(blob => {

            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob); // Create an object URL for the Blob
            link.download = 'qr-code.png'; // Set the file name
            link.click(); // Trigger the download
        })
        .catch(error => {
            console.error('Error fetching QR code:', error);
        });
}
