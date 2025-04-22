import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim

class RLPokemonAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        """
        Inizializza l'agente RL con i parametri principali.

        Args:
            state_size (int): Dimensione dello spazio degli stati.
            action_size (int): Dimensione dello spazio delle azioni.
            learning_rate (float): Tasso di apprendimento.
            gamma (float): Fattore di sconto per il futuro reward.
            epsilon (float): Probabilità iniziale per l'esplorazione.
            epsilon_decay (float): Decadimento di epsilon ad ogni episodio.
            epsilon_min (float): Valore minimo di epsilon.
        """
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.learning_rate = learning_rate

        # Rete neurale per apprendere la policy
        self.model = self._build_model()

        # Ottimizzatore
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def _build_model(self):
        """
        Costruisce una rete neurale semplice per apprendere la policy.
        """
        return nn.Sequential(
            nn.Linear(self.state_size, 260),
            nn.ReLU(),
            nn.Linear(260, 260),
            nn.ReLU(),
            nn.Linear(260, self.action_size)
        )

    def act(self, state):
        """
        Decide un'azione basata sullo stato corrente.

        Args:
            state (np.array): Stato corrente.

        Returns:
            int: Azione selezionata.
        """
        # Esplora o sfrutta
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Esplora
        state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Converte lo stato in tensor
        with torch.no_grad():
            q_values = self.model(state_tensor)
        return torch.argmax(q_values).item()  # Azione con il massimo valore Q

    def train(self, state, action, reward, next_state, done):
        """
        Aggiorna la rete neurale basata sull'esperienza.

        Args:
            state (np.array): Stato corrente.
            action (int): Azione eseguita.
            reward (float): Reward ricevuto.
            next_state (np.array): Stato successivo.
            done (bool): Se l'episodio è terminato.
        """
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
        action_tensor = torch.LongTensor([action])
        reward_tensor = torch.FloatTensor([reward])

        # Valore Q corrente
        current_q = self.model(state_tensor).gather(1, action_tensor.unsqueeze(1))

        # Valore Q target
        with torch.no_grad():
            next_q = self.model(next_state_tensor).max(1)[0]
        target_q = reward_tensor + (self.gamma * next_q * (1 - done))

        # Perdita
        loss = nn.MSELoss()(current_q, target_q.unsqueeze(1))

        # Ottimizzazione
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Aggiornamento di epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
