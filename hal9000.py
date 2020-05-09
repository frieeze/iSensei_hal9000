
import numpy as np
from random import randint
import copy

from keras.models import Sequential, load_model
from keras.layers.core import Dense
from keras.layers import Flatten
from keras.optimizers import Adam

# Init your variables here

model = None
won = 0
lost = 0
equality = 0
gameBoards = np.array([])
winnerHistory = []
SIZE = 7
MIDDLE = 3
WIN = 5

# Put your bot name here
name = "HAL9000"


def makeModel():
    global model
    if model != None:
        return
    try:
        model = load_model("hal9kModel.h5")
        return
    except OSError:
        print('Model File not found, creating model ...')

    model = Sequential()

    model.add(Dense(units=200, input_shape=(7, 7,), activation='relu'))
    model.add(Dense(units=128, activation='relu',
                    kernel_initializer='glorot_uniform'))
    model.add(Dense(units=128, activation='relu',
                    kernel_initializer='glorot_uniform'))
    model.add(Dense(units=128, activation='relu',
                    kernel_initializer='glorot_uniform'))
    model.add(Dense(units=7, activation='sigmoid',
                    kernel_initializer='glorot_uniform'))

    model.compile(loss='binary_crossentropy', optimizer='adam')


def play(board, available_cells, player):
    global model
    makeModel()
    #print("Player ", player)
    # if randint(0, 5) == 0:
    #    return available_cells[randint(0, len(available_cells)-1)]
    predict = []
    for i in available_cells:
        [x, y] = i
        tmpBoard = copy.deepcopy(board)
        tmpBoard[x][y] = player
        predict.append(tmpBoard)
    prob_to_win = model.predict(
        np.array(predict), verbose=0)
    best = int(np.argmax(prob_to_win)/49)
    # print()
    # print("Best move is", available_cells[best],
    #      "with probability to win: ", prob_to_win.max())
    return available_cells[best]


def saveGames(board):
    global gameBoards
    if gameBoards.size == 0:
        gameBoards = np.array([board])
    else:
        gameBoards = np.append(
            gameBoards, [board], axis=0)


def train():
    global model, gameBoards, winnerHistory
    makeModel()
    model.fit(gameBoards, np.array(winnerHistory),
              epochs=5, shuffle=False, verbose=1)
    model.save("hal9kModel.h5")


makeModel()
