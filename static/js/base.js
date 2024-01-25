function showError(message){
    var errorModal = document.getElementById('error-modal')
    errorModal.querySelector('.modal-body').textContent = message
    errorModal.showModal()
}

function showSuccess(message){
    var successModal = document.getElementById('success-modal')
    successModal.querySelector('.modal-body').textContent = message
    successModal.showModal()
}