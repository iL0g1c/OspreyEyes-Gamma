# get logged off stops
# save player logoff stops
# get logged on players
# run clusterering algorithm
# update confidence ratios
from pymongo import MongoClient, UpdateOne
import os
from dotenv import load_dotenv
from operator import itemgetter
from datetime import datetime
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

class ClusterTracker:
    def __init__(self, epsilon, min_samples):
        self.dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
        self.userAssociations = {}
        
        self.playerData = np.empty((0, 2))
        self.usersGoingOffline = []
        self.usersComingOnline = []
        self.newAccounts = []
        self.currentOnlineUsers = []
        self.usersInDatabase = []
        self.users = []

        # MongoDB connection
        load_dotenv()
        password = os.environ.get("MONGODB_PWD")
        connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
        client = MongoClient(connection_string)
        OspreyEyes = client["OspreyEyes"]
        self.activity = OspreyEyes["clusterer"]

    def updatePlayerData(self, users):
        self.users = users

    def getOfflinePlayers(self):
        # update users that came online
        self.currentOnlineUsers = list(map(itemgetter("acid"), self.users))
        self.usersInDatabase = list(self.activity.find({"acid": {"$in": self.currentOnlineUsers}}))
        updateOperations = []
        self.usersGoingOffline = []
        for accountData in self.usersInDatabase:
            if (accountData["currentStatus"] == 0):
                for user in self.users:
                    if user["acid"] == accountData["acid"]:
                        self.usersGoingOffline.append(user)
                        break
                updateOperations.append(
                    UpdateOne(
                        {"acid": accountData["acid"]},
                        {"$set": {
                            "currentStatus": 1,
                        }}
                    )
                )
        if updateOperations:
            self.activity.bulk_write(updateOperations)
        
    def getOnlinePlayers(self):
        # update users that went offline
        currentOfflineUsers = list(self.activity.find({"currentStatus": 1}))
        updateOperations = []
        self.usersComingOnline = []
        for accountData in currentOfflineUsers:
            if accountData["acid"] not in self.currentOnlineUsers:
                for user in self.users:
                    if user["acid"] == accountData["acid"]:
                        self.usersGoingOffline.append(user)
                        break
                updateOperations.append(
                    UpdateOne(
                        {"acid": accountData["acid"]},
                        {"$set": {
                            "currentStatus": 0
                        }}
                    )
                )
        if updateOperations:
            self.activity.bulk_write(updateOperations)
        

    def getNewPlayers(self):
        # create users that detected online for the first time.
        self.newAccounts = []
        accountIdsInDatabase = list(map(itemgetter("acid"), self.usersInDatabase))
        for user in self.users:
            if user["acid"] not in accountIdsInDatabase and user["acid"] != None and isinstance(user["acid"], int) and user["cs"] != "":
                self.newAccounts.append({
                    "acid": user["acid"],
                    "currentStatus": 1,
                })
        if self.newAccounts:
            self.activity.insert_many(self.newAccounts)
        
    def cluster(self):
        self.playerData = np.empty((0, 2))
        for user in self.usersGoingOffline:
            if (isinstance(user["acid"], int)):
                userArray = np.array([[
                    int(user["acid"]),
                    int(user["co"][0]),
                    int(user["co"][1])
                ]])
                if self.playerData.size == 0:
                    self.playerData = userArray
                else:
                    self.playerData = np.append(self.playerData, userArray, axis=0)
        for user in self.usersComingOnline:   
            if (isinstance(user["acid"], int)):
                userArray = np.array([[
                    int(user["acid"]),
                    int(user["co"][0]),
                    int(user["co"][1])
                ]])
                if self.playerData.size == 0:
                    self.playerData = userArray
                else:
                    self.playerData = np.append(self.playerData, userArray, axis=0)

        print(self.playerData)

        # X = self.playerData[:, 2:]
        # X = StandardScaler().fit_transform(X)
        # labels = self.dbscan.fit_predict(X)

        # for i, label in enumerate(labels):
        #     user_id = self.playerData[i, 2]
        #     if label not in self.userAssociations:
        #         self.userAssociations[label] = {user_id}
        #     else:
        #         self.userAssociations[label].add(user_id)
        
        # print(self.userAssociations)