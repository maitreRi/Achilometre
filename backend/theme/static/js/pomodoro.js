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
    if (!statusEl) return;

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
    let secondsLeft, sessionLabel;

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

  if (!document.getElementById('pomodoro-form')) return;

  const startWorkSound = new Audio('/static/sounds/start_work.mp3');
  const endWorkSound = new Audio('/static/sounds/end_work.mp3');
  let lastSessionLabel = null;

  const form = document.getElementById('pomodoro-form');
  const workInput = document.getElementById('work-duration');
  const breakInput = document.getElementById('break-duration');
  const repetitionsInput = document.getElementById('repetitions');
  const infiniteCheckbox = document.getElementById('infinite');
  const totalDurationDisplay = document.getElementById('total-duration-display');
  const timerDisplay = document.getElementById('pomodoro-timer');
  const startBtn = document.getElementById('startPomodoro');
  const stopBtn = document.getElementById('stopPomodoro');

  let timerInterval = null;
  let currentSessionType = null;

  function updateTotalDuration() {
    const work = parseInt(workInput.value) || 25;
    const brk = parseInt(breakInput.value) || 5;
    const reps = parseInt(repetitionsInput.value) || 4;
    const infinite = infiniteCheckbox.checked;

    if (infinite) {
      totalDurationDisplay.textContent = "Durée totale : ∞ (mode infini)";
    } else {
      const totalMin = (work + brk) * reps - brk;
      totalDurationDisplay.textContent = `Durée totale : ${totalMin} min`;
    }
  }

  workInput.addEventListener('input', updateTotalDuration);
  breakInput.addEventListener('input', updateTotalDuration);
  repetitionsInput.addEventListener('input', updateTotalDuration);
  infiniteCheckbox.addEventListener('change', updateTotalDuration);
  updateTotalDuration();

  function clearTimer() {
    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }
  }

  function showRunningState(isRunning) {
    startBtn.classList.toggle('hidden', isRunning);
    stopBtn.classList.toggle('hidden', !isRunning);
    timerDisplay.classList.toggle('hidden', !isRunning);
    totalDurationDisplay.classList.toggle('hidden', isRunning);
  }

  function stopSession() {
    clearTimer();
    localStorage.removeItem(STORAGE_KEY);
    timerDisplay.textContent = "Session arrêtée";
    showRunningState(false);
  }

  function startSession() {
    const work = parseInt(workInput.value) || 25;
    const brk = parseInt(breakInput.value) || 5;
    const reps = parseInt(repetitionsInput.value) || 4;
    const infinite = infiniteCheckbox.checked;

    const state = {
      running: true,
      startedAt: Date.now(),
      workDuration: work,
      breakDuration: brk,
      repetitions: reps,
      infinite: infinite,
    };

    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    showRunningState(true);
    updateTimer(true);
    timerInterval = setInterval(updateTimer, 1000);
  }

  function updateTimer(isInitial = false) {
    const stateRaw = localStorage.getItem(STORAGE_KEY);
    if (!stateRaw) {
      timerDisplay.textContent = "Pas de session active";
      showRunningState(false);
      clearTimer();
      return;
    }

    let state;
    try {
      state = JSON.parse(stateRaw);
    } catch {
      timerDisplay.textContent = "Erreur lecture session";
      clearTimer();
      return;
    }

    if (!state.running) {
      timerDisplay.textContent = "Pas de session active";
      showRunningState(false);
      clearTimer();
      return;
    }

    const now = Date.now();
    const elapsed = Math.floor((now - state.startedAt) / 1000);
    const workSec = state.workDuration * 60;
    const breakSec = state.breakDuration * 60;
    const cycleSec = workSec + breakSec;
    const cyclesCompleted = Math.floor(elapsed / cycleSec);

    if (!state.infinite && cyclesCompleted >= state.repetitions) {
      stopSession();
      timerDisplay.textContent = "Session terminée";
      return;
    }

    const cycleElapsed = elapsed % cycleSec;
    let label, secondsLeft;
    if (cycleElapsed < workSec) {
      label = "Travail";
      secondsLeft = workSec - cycleElapsed;
    } else {
      label = "Pause";
      secondsLeft = cycleSec - cycleElapsed;
    }

    if (label !== currentSessionType || isInitial) {
      if (currentSessionType !== null) {
        endWorkSound.currentTime = 0;
        endWorkSound.play().catch(() => {});
      }
      startWorkSound.currentTime = 0;
      startWorkSound.play().catch(() => {});
      currentSessionType = label;
    }

    timerDisplay.textContent = `${formatTime(secondsLeft)}`;
    document.getElementById('session-status').textContent = `Statut : ${label}`;
    document.getElementById('session-status').classList.remove('hidden');
    document.getElementById('session-repeat').textContent = `Cycle : ${state.infinite ? '∞' : cyclesCompleted + 1} / ${state.repetitions}`;
    document.getElementById('session-repeat').classList.remove('hidden');
  }

  startBtn.addEventListener('click', e => {
    e.preventDefault();
    startSession();
  });

  stopBtn.addEventListener('click', e => {
    e.preventDefault();
    stopSession();
  });

  window.addEventListener('load', () => {
    const stateRaw = localStorage.getItem(STORAGE_KEY);
    if (stateRaw) {
      const state = JSON.parse(stateRaw);
      if (state.running) {
        showRunningState(true);
        updateTimer(true);
        timerInterval = setInterval(updateTimer, 1000);
        return;
      }
    }
    showRunningState(false);
  });
})();
