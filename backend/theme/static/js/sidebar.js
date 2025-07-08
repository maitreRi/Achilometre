document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.getElementById("mainContent");
  const toggleDesktopBtn = document.getElementById("toggleSidebarDesktop");

  toggleDesktopBtn.addEventListener("click", () => {
    if (window.innerWidth < 768) return;
    sidebar.classList.toggle("reduced");
    mainContent.classList.toggle("sidebar-reduced");
  });
});
