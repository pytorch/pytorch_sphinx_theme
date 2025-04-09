// Override "main" with version variable
document.addEventListener('DOMContentLoaded', function() {
  // Check if this is the "docs" pytorch_project
  const metaElement = document.querySelector('meta[name="pytorch_project"]');
  console.log("PyTorch Project:", metaElement);
  if (!metaElement || metaElement.getAttribute('content') !== 'docs') {
    return; // Exit early if not the pytorch docs project
  }
  const version = document.documentElement.getAttribute('data-version');

  // Function to check and update buttons
  function updateButtons() {
    const buttons = document.querySelectorAll('.version-switcher__button');
    let found = false;

    buttons.forEach(btn => {
      console.log("Found button:", btn.innerText);
      if (btn.innerText.includes('main')) {
        btn.innerText = btn.innerText.replace('main', version);
        if (btn.hasAttribute('data-active-version-name')) {
          btn.setAttribute('data-active-version-name',
                          btn.getAttribute('data-active-version-name').replace('main', version));
        }
        found = true;
      }
    });

    // If not found, try again after a delay
    if (!found && attempts < 10) {
      attempts++;
      setTimeout(updateButtons, 500);
    }
  }

  let attempts = 0;
  updateButtons();
});
