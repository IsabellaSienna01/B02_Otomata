const presetSelector = document.getElementById('preset-selector');
const statesInput = document.getElementById('states');
const inputAlphabetInput = document.getElementById('input-alphabet');
const stackAlphabetInput = document.getElementById('stack-alphabet');
const startStateInput = document.getElementById('start-state');
const startStackInput = document.getElementById('start-stack');
const acceptStatesInput = document.getElementById('accept-states');
const transitionsInput = document.getElementById('transitions');
const acceptMethodRadios = document.getElementsByName('accept-method');

const testStringInput = document.getElementById('test-string');
const startSimBtn = document.getElementById('start-sim-btn');
const fastRunBtn = document.getElementById('fast-run-btn');
const simStatus = document.getElementById('sim-status');

const stepPrevBtn = document.getElementById('step-prev');
const stepNextBtn = document.getElementById('step-next');
const autoPlayBtn = document.getElementById('auto-play-btn');
const inputTapeContainer = document.getElementById('input-tape');
const currentStateDisplay = document.getElementById('current-state');
const stackContainer = document.getElementById('stack-container');
const transitionLog = document.getElementById('transition-log');

let pdaConfig = {};

let simulationPath = []; 
let currentStepIndex = 0;
let currentSimulatedInput = "";
let autoPlayInterval = null;


const presets = {
    anbn_fs: {
        states: "q0,q1,q2,q3",
        inputAlphabet: "a,b",
        stackAlphabet: "Z,A",
        startState: "q0",
        startStack: "Z",
        acceptStates: "q3",
        acceptMethod: "final_state",
        transitions: "q0,e,Z->q1,Z\nq1,a,Z->q1,AZ\nq1,a,A->q1,AA\nq1,b,A->q2,e\nq2,b,A->q2,e\nq2,e,Z->q3,Z"
    },
    anbn_es: {
        states: "q0,q1,q2",
        inputAlphabet: "a,b",
        stackAlphabet: "Z,A",
        startState: "q0",
        startStack: "Z",
        acceptStates: "",
        acceptMethod: "empty_stack",
        transitions: "q0,e,Z->q1,Z\nq1,a,Z->q1,AZ\nq1,a,A->q1,AA\nq1,b,A->q2,e\nq2,b,A->q2,e\nq1,e,Z->q1,e\nq2,e,Z->q2,e"
    },
    parentheses_fs: {
        states: "q0,q1,q2",
        inputAlphabet: "(,)",
        stackAlphabet: "Z,(",
        startState: "q0",
        startStack: "Z",
        acceptStates: "q2",
        acceptMethod: "final_state",
        transitions: "q0,e,Z->q1,Z\nq1,(,Z->q1,(Z\nq1,(,(->q1,((\nq1,),(->q1,e\nq1,e,Z->q2,Z"
    },
    parentheses_es: {
        states: "q0",
        inputAlphabet: "(,)",
        stackAlphabet: "Z,(",
        startState: "q0",
        startStack: "Z",
        acceptStates: "",
        acceptMethod: "empty_stack",
        transitions: "q0,(,Z->q0,(Z\nq0,(,(->q0,((\nq0,),(->q0,e\nq0,e,Z->q0,e"
    },
    palindrome_fs: {
        states: "q0,q1,q2",
        inputAlphabet: "a,b,c",
        stackAlphabet: "Z,A,B",
        startState: "q0",
        startStack: "Z",
        acceptStates: "q2",
        acceptMethod: "final_state",
        transitions: "q0,a,Z->q0,AZ\nq0,b,Z->q0,BZ\nq0,a,A->q0,AA\nq0,b,A->q0,BA\nq0,a,B->q0,AB\nq0,b,B->q0,BB\nq0,c,Z->q1,Z\nq0,c,A->q1,A\nq0,c,B->q1,B\nq1,a,A->q1,e\nq1,b,B->q1,e\nq1,e,Z->q2,Z"
    },
    palindrome_es: {
        states: "q0,q1",
        inputAlphabet: "a,b,c",
        stackAlphabet: "Z,A,B",
        startState: "q0",
        startStack: "Z",
        acceptStates: "",
        acceptMethod: "empty_stack",
        transitions: "q0,a,Z->q0,AZ\nq0,b,Z->q0,BZ\nq0,a,A->q0,AA\nq0,b,A->q0,BA\nq0,a,B->q0,AB\nq0,b,B->q0,BB\nq0,c,Z->q1,Z\nq0,c,A->q1,A\nq0,c,B->q1,B\nq1,a,A->q1,e\nq1,b,B->q1,e\nq1,e,Z->q1,e"
    },
    even_palindrome_fs: {
        states: "q0,q1,q2",
        inputAlphabet: "a,b",
        stackAlphabet: "Z,A,B",
        startState: "q0",
        startStack: "Z",
        acceptStates: "q2",
        acceptMethod: "final_state",
        transitions: "q0,a,Z->q0,AZ\nq0,b,Z->q0,BZ\nq0,a,A->q0,AA\nq0,b,A->q0,BA\nq0,a,B->q0,AB\nq0,b,B->q0,BB\nq0,e,Z->q1,Z\nq0,e,A->q1,A\nq0,e,B->q1,B\nq1,a,A->q1,e\nq1,b,B->q1,e\nq1,e,Z->q2,Z"
    },
    even_palindrome_es: {
        states: "q0,q1",
        inputAlphabet: "a,b",
        stackAlphabet: "Z,A,B",
        startState: "q0",
        startStack: "Z",
        acceptStates: "",
        acceptMethod: "empty_stack",
        transitions: "q0,a,Z->q0,AZ\nq0,b,Z->q0,BZ\nq0,a,A->q0,AA\nq0,b,A->q0,BA\nq0,a,B->q0,AB\nq0,b,B->q0,BB\nq0,e,Z->q1,Z\nq0,e,A->q1,A\nq0,e,B->q1,B\nq1,a,A->q1,e\nq1,b,B->q1,e\nq1,e,Z->q1,e"
    }
};

let currentPresetBase = 'anbn';

presetSelector.addEventListener('change', (e) => {
    const key = e.target.value;
    if (key) {
        currentPresetBase = key;
        let method = 'fs';
        Array.from(acceptMethodRadios).forEach(radio => {
            if (radio.checked) method = radio.value === 'final_state' ? 'fs' : 'es';
        });
        const fullKey = `${key}_${method}`;
        if (presets[fullKey]) {
            loadPreset(presets[fullKey]);
        }
    }
});

Array.from(acceptMethodRadios).forEach(radio => {
    radio.addEventListener('change', (e) => {
        if (currentPresetBase) {
            let method = e.target.value === 'final_state' ? 'fs' : 'es';
            const fullKey = `${currentPresetBase}_${method}`;
            if (presets[fullKey]) {
                loadPreset(presets[fullKey]);
            }
        }
    });
});

function loadPreset(preset) {
    statesInput.value = preset.states;
    inputAlphabetInput.value = preset.inputAlphabet;
    stackAlphabetInput.value = preset.stackAlphabet;
    startStateInput.value = preset.startState;
    startStackInput.value = preset.startStack;
    acceptStatesInput.value = preset.acceptStates;
    transitionsInput.value = preset.transitions;
    
    Array.from(acceptMethodRadios).forEach(radio => {
        radio.checked = (radio.value === preset.acceptMethod);
    });
}

function parseConfig() {
    const states = statesInput.value.split(',').map(s => s.trim()).filter(s => s);
    const inputAlphabet = inputAlphabetInput.value.split(',').map(s => s.trim()).filter(s => s);
    const stackAlphabet = stackAlphabetInput.value.split(',').map(s => s.trim()).filter(s => s);
    const startState = startStateInput.value.trim();
    const startStack = startStackInput.value.trim();
    const acceptStates = acceptStatesInput.value.split(',').map(s => s.trim()).filter(s => s);
    let acceptMethod = 'final_state';
    Array.from(acceptMethodRadios).forEach(radio => {
        if (radio.checked) acceptMethod = radio.value;
    });

    const transitionsRaw = transitionsInput.value.split('\n').map(s => s.trim()).filter(s => s);
    const transitions = [];

    for (let t of transitionsRaw) {
        let parts = t.split('->');
        if (parts.length !== 2) continue;
        let left = parts[0].split(',').map(s => s.trim());
        let right = parts[1].split(',').map(s => s.trim());
        
        if (left.length === 3 && right.length === 2) {
            transitions.push({
                fromState: left[0],
                inputStr: left[1],
                popStr: left[2],
                toState: right[0],
                pushStr: right[1] === 'e' ? '' : right[1]
            });
        }
    }

    pdaConfig = {
        states, inputAlphabet, stackAlphabet, startState, startStack, acceptStates, acceptMethod, transitions
    };
    
    return true;
}

document.getElementById('apply-config-btn').addEventListener('click', () => {
    parseConfig();
    alert('Konfigurasi mesin berhasil diterapkan!');
});

function runSimulation(inputString) {
    if (!parseConfig()) return null;

    let queue = [{
        state: pdaConfig.startState,
        stack: pdaConfig.startStack,
        inputRemaining: inputString,
        inputConsumed: "",
        pathLog: [],
        step: 0
    }];

    let maxSteps = 1000;
    let stepCount = 0;
    let bestRejectPath = null;
    
    while (queue.length > 0 && stepCount < maxSteps) {
        stepCount++;
        let current = queue.shift();

        let isAccepted = false;
        if (current.inputRemaining === "") {
            if (pdaConfig.acceptMethod === 'final_state' && pdaConfig.acceptStates.includes(current.state)) {
                isAccepted = true;
            } else if (pdaConfig.acceptMethod === 'empty_stack' && current.stack === "") {
                isAccepted = true;
            }
        }

        if (isAccepted) {
            return { accepted: true, finalState: current };
        }

        if (!bestRejectPath || current.inputConsumed.length > bestRejectPath.inputConsumed.length) {
            bestRejectPath = current;
        }

        let nextStatesGenerated = false;
        for (let t of pdaConfig.transitions) {
            if (t.fromState === current.state) {
                let inputMatch = false;
                let charConsumed = "";
                let remInput = current.inputRemaining;
                
                if (t.inputStr === 'e') {
                    inputMatch = true;
                } else if (remInput.startsWith(t.inputStr)) {
                    inputMatch = true;
                    charConsumed = t.inputStr;
                    remInput = remInput.substring(t.inputStr.length);
                }

                if (inputMatch) {
                    let stackMatch = false;
                    let newStack = current.stack;
                    if (t.popStr === 'e') {
                        stackMatch = true;
                        newStack = t.pushStr + newStack;
                    } else if (current.stack.startsWith(t.popStr)) {
                        stackMatch = true;
                        newStack = t.pushStr + current.stack.substring(t.popStr.length);
                    }

                    if (stackMatch) {
                        nextStatesGenerated = true;
                        let transitionLogStr = `δ(${current.state}, ${t.inputStr}, ${t.popStr}) -> (${t.toState}, ${t.pushStr === '' ? 'e' : t.pushStr})`;
                        queue.push({
                            state: t.toState,
                            stack: newStack,
                            inputRemaining: remInput,
                            inputConsumed: current.inputConsumed + charConsumed,
                            pathLog: [...current.pathLog, {
                                state: current.state,
                                stack: current.stack,
                                inputRemaining: current.inputRemaining,
                                transitionStr: transitionLogStr,
                                nextState: t.toState,
                                newStack: newStack,
                                charConsumed: charConsumed
                            }],
                            step: current.step + 1
                        });
                    }
                }
            }
        }
    }

    return { accepted: false, finalState: bestRejectPath };
}

startSimBtn.addEventListener('click', () => {
    let inputStr = testStringInput.value.trim();
    let result = runSimulation(inputStr);
    
    if (!result) return;
    
    simulationPath = [];
    let stateInfo = result.finalState;
    if (stateInfo.pathLog.length === 0) {
        simulationPath.push({
            state: stateInfo.state,
            stack: stateInfo.stack,
            inputRemaining: stateInfo.inputRemaining,
            inputConsumed: "",
            logMsg: "Start Simulation",
            status: result.accepted ? "accepted" : "rejected"
        });
    } else {
        for (let i = 0; i < stateInfo.pathLog.length; i++) {
            let log = stateInfo.pathLog[i];
            simulationPath.push({
                state: log.state,
                stack: log.stack,
                inputRemaining: log.inputRemaining,
                inputConsumed: stateInfo.inputConsumed.substring(0, stateInfo.inputConsumed.length - log.inputRemaining.length + inputStr.length),
                logMsg: log.transitionStr,
                status: "processing"
            });
        }
        simulationPath.push({
            state: stateInfo.state,
            stack: stateInfo.stack,
            inputRemaining: stateInfo.inputRemaining,
            inputConsumed: stateInfo.inputConsumed,
            logMsg: result.accepted ? "Accepted!" : "Rejected - No valid transitions",
            status: result.accepted ? "accepted" : "rejected"
        });
    }

    currentStepIndex = 0;
    currentSimulatedInput = inputStr;
    
    if (autoPlayInterval) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
        if (autoPlayBtn) autoPlayBtn.textContent = '▶ Auto Play';
    }

    updateVisualizer(currentSimulatedInput);
    
    simStatus.textContent = result.accepted ? "STRING DITERIMA" : "STRING DITOLAK";
    simStatus.className = `status-badge ${result.accepted ? 'accepted' : 'rejected'}`;
});

if (fastRunBtn) {
    fastRunBtn.addEventListener('click', () => {
        let inputStr = testStringInput.value.trim();
        let result = runSimulation(inputStr);
        if (!result) return;
        
        simStatus.textContent = result.accepted ? "STRING DITERIMA" : "STRING DITOLAK";
        simStatus.className = `status-badge ${result.accepted ? 'accepted' : 'rejected'}`;
        alert(result.accepted ? "Sukses: String diterima oleh PDA." : "Gagal: String ditolak oleh PDA.");
    });
}

function updateVisualizer(originalInput) {
    if (simulationPath.length === 0) return;
    
    stepPrevBtn.disabled = (currentStepIndex === 0);
    stepNextBtn.disabled = (currentStepIndex === simulationPath.length - 1);

    let currentConfig = simulationPath[currentStepIndex];

    inputTapeContainer.innerHTML = '';
    let chars = originalInput.split('');
    let consumedLen = originalInput.length - currentConfig.inputRemaining.length;
    
    if (chars.length === 0) {
         let cell = document.createElement('div');
         cell.className = 'tape-cell active';
         cell.textContent = 'e';
         inputTapeContainer.appendChild(cell);
    } else {
        chars.forEach((c, idx) => {
            let cell = document.createElement('div');
            cell.className = 'tape-cell';
            if (idx === consumedLen) {
                cell.classList.add('active');
            } else if (idx < consumedLen) {
                cell.style.opacity = '0.3';
            }
            cell.textContent = c;
            inputTapeContainer.appendChild(cell);
        });
        
        if (consumedLen === chars.length) {
            let cell = document.createElement('div');
            cell.className = 'tape-cell active';
            cell.textContent = 'e';
            inputTapeContainer.appendChild(cell);
        }
    }

    currentStateDisplay.textContent = currentConfig.state;
    if (currentConfig.status === 'accepted') {
        currentStateDisplay.classList.add('accepted-state');
    } else {
        currentStateDisplay.classList.remove('accepted-state');
    }

    stackContainer.innerHTML = '';
    let stackChars = currentConfig.stack.split('');
    if (stackChars.length === 0 || currentConfig.stack === "") {
        let el = document.createElement('div');
        el.className = 'stack-item';
        el.style.opacity = '0.5';
        el.textContent = '(empty)';
        stackContainer.appendChild(el);
    } else {
        stackChars.forEach(c => {
            let el = document.createElement('div');
            el.className = 'stack-item';
            el.textContent = c;
            stackContainer.appendChild(el);
        });
    }

    transitionLog.innerHTML = '';
    for (let i = 0; i <= currentStepIndex; i++) {
        let li = document.createElement('li');
        li.className = 'log-item';
        li.textContent = `Step ${i}: ${simulationPath[i].logMsg}`;
        if (simulationPath[i].status === 'accepted') li.classList.add('success');
        if (simulationPath[i].status === 'rejected') li.classList.add('error');
        transitionLog.appendChild(li);
    }
    transitionLog.scrollTop = transitionLog.scrollHeight;
}

stepPrevBtn.addEventListener('click', () => {
    if (currentStepIndex > 0) {
        currentStepIndex--;
        updateVisualizer(currentSimulatedInput);
    }
});

stepNextBtn.addEventListener('click', () => {
    if (currentStepIndex < simulationPath.length - 1) {
        currentStepIndex++;
        updateVisualizer(currentSimulatedInput);
    }
});

if (autoPlayBtn) {
    autoPlayBtn.addEventListener('click', () => {
        if (simulationPath.length === 0) return;
        
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
            autoPlayInterval = null;
            autoPlayBtn.textContent = '▶ Auto Play';
        } else {
            if (currentStepIndex === simulationPath.length - 1) {
                currentStepIndex = 0; 
                updateVisualizer(currentSimulatedInput);
            }
            autoPlayBtn.textContent = '⏸ Pause';
            autoPlayInterval = setInterval(() => {
                if (currentStepIndex < simulationPath.length - 1) {
                    currentStepIndex++;
                    updateVisualizer(currentSimulatedInput);
                } else {
                    clearInterval(autoPlayInterval);
                    autoPlayInterval = null;
                    autoPlayBtn.textContent = '▶ Auto Play';
                }
            }, 1000);
        }
    });
}

presetSelector.value = '';
currentPresetBase = '';
