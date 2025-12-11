document.querySelectorAll('.input-field').forEach(input => {
    // Validate on blur (when user clicks away)
    input.addEventListener('blur', async () => {
        const num = parseInt(input.getAttribute('data-num')); // Convert to integer
        const field = input.getAttribute('data-field');
        const value = input.value.trim();

        if (value === '') return; // Skip validation if input is empty

        const response = await fetch('/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ num, field, value })
        });
        const result = await response.json();
        console.log(`Validation for num=${num}, field=${field}, value=${value}:`, result);

        input.classList.remove('correct', 'incorrect', 'idk');
        if (result.valid === true) {
            input.classList.add('correct');
        } else if (result.valid === false) {
            input.classList.add('incorrect');
        }
    });

    // Validate on Enter key press
    input.addEventListener('keydown', async (event) => {
        if (event.key === 'Enter') {
            const num = parseInt(input.getAttribute('data-num')); // Convert to integer
            const field = input.getAttribute('data-field');
            const value = input.value.trim();

            if (value === '') return; // Skip validation if input is empty

            const response = await fetch('/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num, field, value })
            });
            const result = await response.json();
            console.log(`Validation for num=${num}, field=${field}, value=${value}:`, result);

            input.classList.remove('correct', 'incorrect', 'idk');
            if (result.valid === true) {
                input.classList.add('correct');
            } else if (result.valid === false) {
                input.classList.add('incorrect');
            }
        }
    });
});

document.querySelectorAll('.idk-btn').forEach(button => {
    button.addEventListener('click', async () => {
        const num = parseInt(button.getAttribute('data-num'));

        const response = await fetch(`/answer/${num}`);
        const data = await response.json();

        const row = button.closest('.quiz-row');
        const inputs = row.querySelectorAll('.input-field');
        inputs[0].value = data.first;
        inputs[1].value = data.last;
        inputs[2].value = data.start;
        inputs[3].value = data.end;
        inputs[4].value = data.party;

        inputs.forEach(input => {
            input.classList.remove('correct', 'incorrect');
            input.classList.add('idk');
        });
    });
});
