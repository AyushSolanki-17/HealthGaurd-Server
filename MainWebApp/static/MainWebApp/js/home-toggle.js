function loginclick() {
    document.getElementById('login-form').style.display = 'flex';
    document.getElementById('signup-form').style.display = 'none';
    document.querySelector('.login-toggle').style.backgroundColor = 'var(--background-secondary)'
    document.querySelector('.signup-toggle').style.backgroundColor = 'var(--black)'
    document.querySelector('.login-toggle').style.color = 'var(--white)'
    document.querySelector('.signup-toggle').style.color = 'var(--sec-green)'

}
function signupclick() {
    document.getElementById('signup-form').style.display = 'flex';
    document.getElementById('login-form').style.display = 'none';
    document.querySelector('.signup-toggle').style.backgroundColor = 'var(--background-secondary)'
    document.querySelector('.login-toggle').style.backgroundColor = 'var(--black)'
    document.querySelector('.signup-toggle').style.color = 'var(--white)'
    document.querySelector('.login-toggle').style.color = 'var(--sec-green)'
}