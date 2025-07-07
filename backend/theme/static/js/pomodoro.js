(function () {
  const STORAGE_KEY = 'pomodoro_state';

  function formatTime(seconds) {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  function updatePomodoroWidget() {
    const stateRaw = localStorage.getItem(STORAGE_KEY);
    const statusEl = document.getElementById('pomodoro-status');

    if (!stateRaw) {
      statusEl.textContent = "Pas de session Pomodoro active";
      return;
    }

    let state;
    try {
      state = JSON.parse(stateRaw);
    } catch {
      statusEl.textContent = "Pas de session Pomodoro active";
      return;
    }

    if (!state.running) {
      statusEl.textContent = "Pas de session Pomodoro active";
      return;
    }

    const now = Date.now();
    const elapsed = Math.floor((now - state.startedAt) / 1000);
    const workDuration = state.workDuration * 60;
    const breakDuration = state.breakDuration * 60;
    const cycleDuration = workDuration + breakDuration;
    let cyclesCompleted = Math.floor(elapsed / cycleDuration);

    if (!state.infinite && cyclesCompleted >= state.repetitions) {
      localStorage.removeItem(STORAGE_KEY);
      statusEl.textContent = "Session Pomodoro terminée";
      return;
    }

    const cycleElapsed = elapsed % cycleDuration;
    let secondsLeft;
    let sessionLabel;

    if (cycleElapsed < workDuration) {
      sessionLabel = "Travail";
      secondsLeft = workDuration - cycleElapsed;
    } else {
      sessionLabel = "Pause";
      secondsLeft = cycleDuration - cycleElapsed;
    }

    const cycleDisplay = state.infinite ? "∞" : (cyclesCompleted + 1) + " / " + state.repetitions;
    statusEl.textContent = `${sessionLabel} - Temps restant : ${formatTime(secondsLeft)} (Cycle ${cycleDisplay})`;
    statusEl.style.color = (sessionLabel === "Pause") ? "green" : "#2563eb";
  }

  setInterval(updatePomodoroWidget, 1000);
  updatePomodoroWidget();
})();
