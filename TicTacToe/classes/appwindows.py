import tkinter as tk
from random import randint
from threading import Timer

from classes.jsonfile import JSONFile
from classes.virtualarea import VirtualArea
from classes.player import Player
from classes.ia import IA

PlayersFile = JSONFile("./resources/players.csv", False)
GameArea = VirtualArea()
Players = list()


class AppWindows(tk.Tk):
    AlreadyOpen = False

    PlayWithBot = False
    DifficultyLevel = 1

    ImgStorage = dict()
    Colors = {
        "lightblue": "#637d96",
        "mediumblue": "#376b8c",
        "darkblue": "#222d5a"
    }

    def __init__(self, fontFamily):
        super().__init__()
        self.FontFamily = fontFamily

    def RunGame(self, firstPlayer, secondPlayer):
        if len(firstPlayer) > 0 and len(secondPlayer) > 0:
            Players.clear()

            tokens = AppWindows.GetRandomTokens()

            AppWindows.SetPlayer(firstPlayer, tokens[0])

            if AppWindows.PlayWithBot:
                Players.append(IA(secondPlayer, tokens[1], AppWindows.DifficultyLevel))
            else:
                AppWindows.SetPlayer(secondPlayer, tokens[1])

            AppWindows.RandomStartPlayer()

            self.DisplayGameArea()
        else:
            self.DisplayGameConfig(AppWindows.PlayWithBot)

    def DisplayMenu(self):
        self.DeleteWindowContent()
        self.SetWindowSettings("Tic Tac Toe")

        label = tk.Label(self, text="Menu Principal", font=("Trebuchet Sans MS", 20), fg="#000")
        btNewGame = self.GetButton(self, "Nouvelle partie")
        btDisplayScores = self.GetButton(self, "Afficher le palmarès", "mediumblue")
        btGameRules = self.GetButton(self, "Règles du jeu", "lightblue")

        btNewGame.configure(command=lambda: self.DisplayEnemyChoice())
        btDisplayScores.configure(command=lambda: self.DisplayScores())
        btGameRules.configure(command=lambda: self.DisplayRules())

        label.pack(pady=5)
        btNewGame.pack(ipady=15, padx=10, pady=5)
        btDisplayScores.pack(ipady=15, padx=10, pady=5)
        btGameRules.pack(ipady=15, padx=10, pady=5)

        self.CenterWindowDisplay()

        if not self.AlreadyOpen:
            self.AlreadyOpen = True
            self.mainloop()

    def DisplayScores(self):
        self.DeleteWindowContent()
        self.SetWindowSettings("La liste des joueurs")

        playerData = PlayersFile.GetContent()

        nameLabel = tk.Label(self, text="Nom du joueur", fg=AppWindows.Colors["mediumblue"],
                             font=(self.FontFamily, 14), pady=10, padx=10)
        scoreLabel = tk.Label(self, text="Score du joueur", fg=AppWindows.Colors["mediumblue"],
                              font=(self.FontFamily, 14), pady=10, padx=10)

        nameLabel.grid(row=0, column=0)
        scoreLabel.grid(row=0, column=1)

        for i in range(len(playerData)):
            nLabel = tk.Label(self, text=playerData[i]["name"], font=(self.FontFamily, 12), pady=5, padx=10)
            sLabel = tk.Label(self, text=playerData[i]["score"], font=(self.FontFamily, 12), pady=5, padx=10)

            nLabel.grid(row=i+1, column=0)
            sLabel.grid(row=i+1, column=1)

        self.CenterWindowDisplay()

    def DisplayRules(self):
        self.DeleteWindowContent()
        self.SetWindowSettings("Les règles du jeu", AppWindows.Colors["lightblue"])

        rulesMessage = "Dans ce jeu, deux joueurs s'affrontent."
        rulesMessage += "\n\nÀ tour de rôle, ils désignent une case et y insèrent alternativement un signe (`X` et `O`)."
        rulesMessage += "\n\nLe premier joueur qui arrive à faire un alignement vertical, horizontal ou diagonal de trois signes gagne la partie."
        rulesMessage += "\n\nSi le plateau de jeu est rempli de signes et qu’il n’y a pas d'alignement de trois, alors c’est un match nul."

        rules = tk.Text(self, bg=AppWindows.Colors["lightblue"], fg="#fff", bd=0, wrap=tk.WORD,
                        font=("Trebuchet MS", 12), height=10)

        rules.insert(tk.INSERT, rulesMessage)
        rules.pack(padx=10, pady=10)

        btnExit = self.GetButton(self, "Fermer")
        btnExit.configure(command=lambda: self.DisplayMenu())
        btnExit.pack(pady=20, ipady=15)

        self.CenterWindowDisplay()

    def DisplayEnemyChoice(self):
        self.DeleteWindowContent()
        self.SetWindowSettings("Choix de l'adversaire")

        btnSinglePlayer = self.GetButton(self, "Jouer contre un Bot")
        btnTwoPlayers = self.GetButton(self, "Jouer contre un autre joueur")

        btnSinglePlayer.configure(command=lambda: self.DisplayBotDifficulty())
        btnTwoPlayers.configure(command=lambda: self.DisplayGameConfig(False))

        btnSinglePlayer.pack(side=tk.LEFT, padx=10, pady=10, ipady=10)
        btnTwoPlayers.pack(side=tk.RIGHT, padx=10, pady=10, ipady=10)

        self.CenterWindowDisplay()

    def DisplayBotDifficulty(self):
        self.DeleteWindowContent()
        self.SetWindowSettings("Niveau de difficulté")

        titleLabel = tk.Label(self, text="Choisissez le niveau de difficulté", fg=AppWindows.Colors["darkblue"],
                              font=(self.FontFamily, 20))

        titleLabel.pack(side=tk.TOP, pady=10)

        buttonsFrame = tk.Frame(self)
        buttonsFrame.pack(side=tk.BOTTOM, padx=5, pady=10)

        btnEasy = self.GetButton(buttonsFrame, "Facile", "lightblue")
        btnMedium = self.GetButton(buttonsFrame, "Moyen", "mediumblue")
        btnHardcore = self.GetButton(buttonsFrame, "Difficile")

        btnEasy.configure(command=lambda: self.SetDifficultyLevel(1))
        btnMedium.configure(command=lambda: self.SetDifficultyLevel(2))
        btnHardcore.configure(command=lambda: self.SetDifficultyLevel(3))

        btnEasy.pack(padx=5, side=tk.LEFT)
        btnMedium.pack(padx=5, side=tk.LEFT)
        btnHardcore.pack(padx=5, side=tk.LEFT)

    def DisplayGameConfig(self, vsBot):
        self.DeleteWindowContent()
        self.SetWindowSettings("Sélection des joueurs")

        AppWindows.PlayWithBot = vsBot

        # FRAME #
        playersFrame = tk.Frame(self)
        firstPlayerFrame = tk.Frame(playersFrame)
        secondPlayerFrame = tk.Frame(playersFrame)

        playersFrame.pack(padx=10, pady=10, side=tk.TOP)
        firstPlayerFrame.pack(side=tk.LEFT, fill=tk.X)
        secondPlayerFrame.pack(side=tk.RIGHT, fill=tk.X)

        # FIRST PLAYER ENTRY #
        if not vsBot:
            fpLabelText = "Nom du premier joueur"
        else:
            fpLabelText = "Nom du joueur"

        firstPlayerName = tk.StringVar()
        firstPlayerLabel = tk.Label(firstPlayerFrame, text=fpLabelText, font=("Trebuchet MS", 14), fg=AppWindows.Colors["darkblue"])
        firstPlayer = tk.Entry(firstPlayerFrame, textvariable=firstPlayerName, width=35, relief=tk.SUNKEN)

        firstPlayerLabel.pack(side=tk.TOP)
        firstPlayer.pack(side=tk.BOTTOM, ipady=5)

        # VERSUS LOGO #
        VsImgFile = "resources/images/versus-logo.png"

        AppWindows.ImgStorage[VsImgFile] = tk.PhotoImage(file=VsImgFile)
        vsLabel = tk.Label(playersFrame, image=AppWindows.ImgStorage[VsImgFile])
        vsLabel.pack(padx=20)

        # SECOND PLAYER ENTRY #
        if not vsBot:
            secondPlayerName = tk.StringVar()
            secondPlayerLabel = tk.Label(secondPlayerFrame, text="Nom du second joueur",
                                         font=("Trebuchet MS", 14), fg=AppWindows.Colors["darkblue"])

            secondPlayer = tk.Entry(secondPlayerFrame, textvariable=secondPlayerName, width=35)

            secondPlayerLabel.pack(side=tk.TOP)
            secondPlayer.pack(side=tk.BOTTOM, ipady=5)
        else:
            secondPlayerName = self.GetRandomName()
            secondPlayerLabel = tk.Label(secondPlayerFrame, text=secondPlayerName, font=("Arial Black", 14), fg="darkred")
            secondPlayerLabel.pack()

        btnPlay = self.GetButton(self, "Jouer")
        btnMenu = self.GetButton(self, "Menu principal", "mediumblue")

        if not vsBot:
            btnPlay.configure(command=lambda: self.RunGame(firstPlayerName.get(), secondPlayerName.get()))
        else:
            btnPlay.configure(command=lambda: self.RunGame(firstPlayerName.get(), secondPlayerName))

        btnMenu.configure(command=lambda: self.DisplayMenu())

        btnPlay.pack(pady=5, ipady=10)
        btnMenu.pack(pady=5, ipady=10)

        self.CenterWindowDisplay()

    def DisplayGameArea(self):
        if AppWindows.IsBot(Players[0]):
            timer = Timer(2, self.BotPlay)
            timer.start()

        self.DeleteWindowContent()
        self.SetWindowSettings("Que le meilleur gagne !", AppWindows.Colors["darkblue"])

        areaCases = GameArea.GetArea()

        bodyFrame = tk.Frame(self, bg=AppWindows.Colors["darkblue"])
        areaFrame = tk.Frame(bodyFrame, bd=1)

        bodyFrame.pack()
        areaFrame.pack(padx=10, pady=10)

        headerFrame = tk.Frame(self)
        currentPlayerLabel = tk.Label(headerFrame, font=(self.FontFamily, 20),
                                      bg=AppWindows.Colors["darkblue"], fg="#fff")

        currentPlayerLabel.configure(text=f"Tour de {Players[0].Name}")

        headerFrame.pack(pady=10)
        currentPlayerLabel.pack()

        for x in range(3):
            for y in range(3):
                if (x == 1 and y == 1) or ((x == 0 or x == 2) and y % 2 == 0):
                    bgColor = AppWindows.Colors["lightblue"]
                else:
                    bgColor = AppWindows.Colors["mediumblue"]

                btn = self.GetAreaButton(areaFrame, x, y, bgColor)
                btn.configure(text=areaCases[x][y])
                btn.grid(row=x, column=y)

        self.CenterWindowDisplay()

    def DisplayCongratulations(self):
        winner = Players[0]

        if not self.IsBot(winner):
            updatedData = list()

            if winner.NewPlayer:
                updatedData.append({
                    "name": winner.Name,
                    "score": 45
                })

                for line in PlayersFile.GetContent():
                    updatedData.append(line)
            else:
                for line in PlayersFile.GetContent():
                    if line["name"] == winner.Name:
                        line["score"] = int(winner.Score) + 45

                    updatedData.append(line)

            PlayersFile.SetContent(updatedData)

        self.DeleteWindowContent()
        self.SetWindowSettings(f"Félicitations {winner.Name} !!!")

        congratsLabel = tk.Label(self, text=f"Félicitation {winner.Name}, tu as gagné !",
                                 fg=AppWindows.Colors["darkblue"], font=(self.FontFamily, 16))
        congratsLabel.pack(padx=20, pady=5)

        if not self.IsBot(winner):
            if winner.NewPlayer:
                scoreLabelText = f"Tu as remporté 45 points."
            else:
                scoreLabelText = f"Ton nouveau score : {winner.Score} + 45 ({winner.Score + 45}) points."

            scoreLabel = tk.Label(self, text=scoreLabelText, fg=AppWindows.Colors["darkblue"], font=(self.FontFamily, 14))
            scoreLabel.pack(padx=20, pady=5)

        btnReplay = self.GetButton(self, "Rejouer")
        btnMenu = self.GetButton(self, "Menu principal")

        btnReplay.configure(command=lambda: self.PlayAgain())
        btnMenu.configure(command=lambda: self.ExitGame())

        btnReplay.pack(pady=5, padx=10)
        btnMenu.pack(pady=5, padx=10)

        GameArea.ResetArea()

        self.CenterWindowDisplay()

    def DisplayNoWinner(self):
        self.DeleteWindowContent()
        self.SetWindowSettings("Retentez votre chance...")

        congratulations = tk.Label(self, text="Match nul !", fg=AppWindows.Colors["darkblue"], font=(self.FontFamily, 26))
        congratulations.pack(padx=20, pady=20)

        btnReplay = self.GetButton(self, "Rejouer")
        btnMenu = self.GetButton(self, "Menu principal")

        btnReplay.configure(command=lambda: self.PlayAgain())
        btnMenu.configure(command=lambda: self.ExitGame())

        btnReplay.pack(pady=5, padx=10)
        btnMenu.pack(pady=5, padx=10)

        GameArea.ResetArea()

        self.CenterWindowDisplay()

    # region METHODS

    def PlayAgain(self):
        GameArea.ResetArea()
        AppWindows.RandomStartPlayer()
        self.DisplayGameArea()

    def ExitGame(self):
        AppWindows.Players = list()
        self.DisplayMenu()

    def DeleteWindowContent(self):
        for child in self.winfo_children():
            child.destroy()

    def CenterWindowDisplay(self):
        self.call("tk::PlaceWindow", self, "center")

    def RandomStartPlayer():
        for i in range(randint(1, 10)):
            Players.reverse()

    RandomStartPlayer = staticmethod(RandomStartPlayer)

    def BotPlay(self):
        iaChoice = Players[0].Play(GameArea.GetArea())
        self.AddToken(iaChoice[0], iaChoice[1])

    def AddToken(self, x, y):
        if GameArea.IsAvailable(x, y):
            GameArea.AddToken(x, y, Players[0].Token)
            area = GameArea.GetArea()
            win = False

            diag1 = (area[0][2], area[1][1], area[2][0])
            diag2 = (area[0][0], area[1][1], area[2][2])

            if AppWindows.CheckWinner(diag1) or AppWindows.CheckWinner(diag2):
                win = True

            if not win:
                for i in range(3):
                    row = (area[i][0], area[i][1], area[i][2])
                    col = (area[0][i], area[1][i], area[2][i])

                    if AppWindows.CheckWinner(row) or AppWindows.CheckWinner(col):
                        win = True
                        break

            if win:
                self.DisplayCongratulations()
            elif GameArea.IsFull():
                self.DisplayNoWinner()
            else:
                Players.reverse()
                self.DisplayGameArea()

    def CheckWinner(lineValues):
        compare = lineValues[0]

        if len(compare) == 0:
            return False

        for value in lineValues:
            if compare != value:
                return False

        return True

    CheckWinner = staticmethod(CheckWinner)

    def IsBot(value):
        return isinstance(value, IA)

    IsBot = staticmethod(IsBot)

    # endregion

    # region SETTERS

    def SetWindowSettings(self, title, bg="SystemButtonFace", geo=""):
        self.title(title)
        self["bg"] = bg

        if len(geo) > 0:
            self.geometry(geo)

    def SetPlayer(playerName, token):
        playersList = PlayersFile.GetContent()
        p = Player(playerName, token)

        if len(playersList) > 0:
            for datas in playersList:
                if datas["name"] == p.Name:
                    p.Score = datas["score"]
                    p.NewPlayer = False
                    break

        Players.append(p)

    SetPlayer = staticmethod(SetPlayer)

    def SetDifficultyLevel(self, level):
        AppWindows.DifficultyLevel = level
        self.DisplayGameConfig(True)

    # endregion

    # region GETTERS

    def GetButton(self, master, text, bgColor="darkblue", width=25):
        return tk.Button(master, width=width, text=text, font=(self.FontFamily, 12),
                         bg=AppWindows.Colors[bgColor], fg="#fff", relief="flat", borderwidth=1, cursor="hand2")

    def GetAreaButton(self, master, x, y, bgColor):
        return tk.Button(master, width=4, height=1, relief="flat", fg="#fff", font=(self.FontFamily, 30), bg=bgColor,
                         cursor="hand2", command=lambda: self.AddToken(x, y))

    def GetRandomName():
        namesList = ["Cédric", "Samir", "Sophie", "Lyham", "Stéphanie", "Léa", "Matteo", "Christian", "Marie"]
        return "{} (BOT)".format(namesList[randint(0, len(namesList)-1)])

    GetRandomName = staticmethod(GetRandomName)

    def GetRandomTokens():
        tokens = ["X", "O"]

        for i in range(randint(1, 10)):
            tokens.reverse()

        return tokens

    GetRandomTokens = staticmethod(GetRandomTokens)

    # endregion
