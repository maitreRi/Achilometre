document.addEventListener('DOMContentLoaded', () => {
  const toggleButton = document.getElementById('dark-mode-toggle');
  const html = document.documentElement;

  if (!toggleButton) return;

  // Appliquer le thème initial
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme === 'dark') {
    html.classList.add('dark');
    toggleButton.innerText = '☀️';
  } else {
    toggleButton.innerText = '🌙';
  }

  toggleButton.addEventListener('click', () => {
    const isDark = html.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    toggleButton.innerText = isDark ? '☀️' : '🌙';
  });
});
