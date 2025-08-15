const boardElement = document.getElementById('board');
if (boardElement) {
    const game = new Chess();
    const board = Chessboard('board', {
        draggable: true,
        pieceTheme: '/static/chessboard/img/chesspieces/{piece}.png',
        position: 'start',
        onDrop: onDrop,
        onSnapEnd: onSnapEnd,
        dropOffBoard: 'snapback'
    });

    /**
     * Called when a piece is dropped on the board.
     * Tries to make the move in the game engine, otherwise snaps back.
     */
    function onDrop(source, target) {
        const move = game.move({
            from: source,
            to: target,
            promotion: 'q'
        });

        // Illegal move
        if (move === null) return 'snapback';

        updateHistory();
    }

    /**
     * Called after the piece snap animation. Updates board to match game state.
     * Ensures castling rook moves alongside the king.
     */
    function onSnapEnd() {
        board.position(game.fen());
    }

    /**
     * Refresh the move history list in the UI.
     */
    function updateHistory() {
        const history = game.history();
        const historyList = document.getElementById('move-history');
        historyList.innerHTML = '';
        history.forEach((move, index) => {
            const li = document.createElement('li');
            li.textContent = move;
            historyList.appendChild(li);
        });
    }

        // Reset button handler
        const resetBtn = document.getElementById('resetBtn');
        if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            game.reset();
            board.start();
            updateHistory();
        });
    }
}
