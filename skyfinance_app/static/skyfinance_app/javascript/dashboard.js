document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('profileDropdownToggle');
  const menu = document.getElementById('profileDropdownMenu');

  if (toggle && menu) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
      if (!menu.contains(e.target) && !toggle.contains(e.target)) {
        menu.classList.remove('show');
      }
    });
  }

  const input = document.getElementById('profilePicInput');
  const preview = document.getElementById('profilePicPreview');
  const removeBtn = document.getElementById('removePicBtn');
  const removeCheckbox = document.getElementById('removePicCheckbox');

  if (input && preview) {
    input.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          preview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (removeBtn && preview && input && removeCheckbox) {
    removeBtn.addEventListener('click', () => {
      preview.src = '/static/skyfinance_app/images/user-profile.svg';
      input.value = '';
      removeCheckbox.checked = true;
    });
  }

  const transactionType = document.getElementById('transaction_type');
  const categoryField = document.getElementById('category-field');

  const toggleCategoryVisibility = () => {
    if (transactionType && categoryField) {
      categoryField.style.display = transactionType.value === 'expense' ? 'block' : 'none';
    }
  };

  toggleCategoryVisibility();
  if (transactionType) {
    transactionType.addEventListener('change', toggleCategoryVisibility);
  }

  const memoInput = document.getElementById('memo');
  const charCounter = document.getElementById('charCount');

  if (memoInput && charCounter) {
    const updateCounter = () => {
      charCounter.textContent = `${memoInput.value.length}/50`;
    };
    updateCounter();
    memoInput.addEventListener('input', updateCounter);
  }
});
