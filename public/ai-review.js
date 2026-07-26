async function triggerAI(action) {
    const firId = document.getElementById('fir-id').value;
    const resultBox = document.getElementById('ai-result');
    
    if (!firId) {
        alert("Please enter an FIR ID");
        return;
    }

    resultBox.style.display = 'block';
    resultBox.textContent = "Processing via Privacy Gateway & Mock AI Provider...";

    try {
        const response = await fetch(`/api/v1/ai/firs/${firId}/${action}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        resultBox.textContent = `Error: ${e.message}`;
    }
}

async function reviewAI(status) {
    const outputId = document.getElementById('output-id').value;
    const feedback = document.getElementById('feedback').value;
    const resultBox = document.getElementById('review-result');
    
    if (!outputId) {
        alert("Please enter an Output ID to review");
        return;
    }

    resultBox.style.display = 'block';
    resultBox.textContent = "Submitting review to audit log...";

    try {
        const response = await fetch(`/api/v1/ai/outputs/${outputId}/review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: status, feedback: feedback })
        });
        
        const data = await response.json();
        resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        resultBox.textContent = `Error: ${e.message}`;
    }
}
