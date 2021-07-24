function showInputField(option) {
        switch (option) {
            case 'once':
                document.getElementById('monthly-billing-container').style.display = 'none'
                document.getElementById('annual-billing-container').style.display = 'none'
                break;
            case 'monthly':
                document.getElementById('annual-billing-container').style.display = 'none'
                document.getElementById('monthly-billing-container').style.display = 'block'
                break;
            case 'annual':
                document.getElementById('monthly-billing-container').style.display = 'none'
                document.getElementById('annual-billing-container').style.display = 'block'
        }
}
