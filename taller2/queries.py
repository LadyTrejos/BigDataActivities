from numpy import nan


def result_table_agg(season, team):
    return [
        {
            "$match": {
                "Season": season,
                "$or": [{"HomeTeam": team}, {"AwayTeam": team}],
            }
        },
        {
            "$facet": {
                "pj": [{"$count": "count"}],
                "pg": [
                    {
                        "$match": {
                            "$or": [
                                {"$and": [{"HomeTeam": team}, {"FTR": "H"}]},
                                {"$and": [{"AwayTeam": team}, {"FTR": "A"}]},
                            ]
                        }
                    },
                    {"$count": "count"},
                ],
                "pp": [
                    {
                        "$match": {
                            "$or": [
                                {"$and": [{"HomeTeam": team}, {"FTR": "A"}]},
                                {"$and": [{"AwayTeam": team}, {"FTR": "H"}]},
                            ]
                        }
                    },
                    {"$count": "count"},
                ],
                "gf": [
                    {
                        "$project": {
                            "_id": 0,
                            "sum": {
                                "$add": [
                                    {
                                        "$cond": {
                                            "if": {"$eq": ["$HomeTeam", team]},
                                            "then": "$FTHG",
                                            "else": {
                                                "$cond": {
                                                    "if": {"$eq": ["$AwayTeam", team]},
                                                    "then": "$FTAG",
                                                    "else": 0,
                                                }
                                            },
                                        }
                                    }
                                ]
                            },
                        }
                    }
                ],
                "gc": [
                    {
                        "$project": {
                            "_id": 0,
                            "sum": {
                                "$add": [
                                    {
                                        "$cond": {
                                            "if": {"$eq": ["$HomeTeam", team]},
                                            "then": "$FTAG",
                                            "else": {
                                                "$cond": {
                                                    "if": {"$eq": ["$AwayTeam", team]},
                                                    "then": "$FTHG",
                                                    "else": 0,
                                                }
                                            },
                                        }
                                    }
                                ]
                            },
                        }
                    }
                ],
            }
        },
        {
            "$project": {
                "PJ": {"$arrayElemAt": ["$pj.count", 0]},
                "PG": {"$arrayElemAt": ["$pg.count", 0]},
                "PP": {"$arrayElemAt": ["$pp.count", 0]},
                "GF": {"$sum": "$gf.sum"},
                "GC": {"$sum": "$gc.sum"},
            }
        },
        {
            "$project": {
                "EQUIPO": team,
                "PJ": 1,
                "PG": 1,
                "PP": 1,
                "GF": 1,
                "GC": 1,
                "PTOS": {
                    "$sum": [
                        {"$subtract": ["$PJ", {"$sum": ["$PG", "$PP"]}]},
                        {"$multiply": ["$PG", 3]},
                    ]
                },
            }
        },
    ]


def goals_avg_agg(season):
    return [
        {"$match": {"Season": season}},
        {
            "$group": {
                "_id": None,
                "mean_ht": {"$avg": "$FTHG"},
                "mean_at": {"$avg": "$FTAG"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "pg": {"$sum": ["$mean_ht", "$mean_at"]},
                "pv": "$mean_at",
                "pl": "$mean_ht",
            }
        },
    ]


def bookings_avg_agg(season):
    return [
        {
            "$match": {
                "Season": season,
                "HY": {"$ne": nan},
                "HR": {"$ne": nan},
                "AY": {"$ne": nan},
                "AR": {"$ne": nan},
            }
        },
        {
            "$group": {
                "_id": None,
                "ptal": {"$avg": "$HY"},
                "ptav": {"$avg": "$AY"},
                "ptrl": {"$avg": "$HR"},
                "ptrv": {"$avg": "$AR"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "pta": {"$sum": ["$ptal", "$ptav"]},
                "ptr": {"$sum": ["$ptrl", "$ptrv"]},
                "ptal": 1,
                "ptav": 1,
                "ptrl": 1,
                "ptrv": 1,
            }
        },
    ]


def shots_on_target_avg_agg(season):
    return [
        {"$match": {"Season": season, "HST": {"$ne": nan}, "AST": {"$ne": nan}}},
        {"$group": {"_id": None, "phst": {"$avg": "$HST"}, "past": {"$avg": "$AST"}}},
        {
            "$project": {
                "_id": 0,
                "phst": 1,
                "past": 1,
                "pst": {"$sum": ["$phst", "$past"]},
            }
        },
    ]


def shots_on_target_agg(season, team):
    return [
        {
            "$match": {
                "Season": season,
                "$or": [{"HomeTeam": team}, {"AwayTeam": team}],
                "HST": {"$ne": nan},
                "AST": {"$ne": nan},
            }
        },
        {
            "$facet": {
                "cstl": [
                    {
                        "$project": {
                            "_id": 0,
                            "sum": {
                                "$add": [
                                    {
                                        "$cond": {
                                            "if": {"$eq": ["$HomeTeam", team]},
                                            "then": "$HST",
                                            "else": {
                                                "$cond": {
                                                    "if": {"$eq": ["$AwayTeam", team]},
                                                    "then": "$AST",
                                                    "else": 0,
                                                }
                                            },
                                        }
                                    }
                                ]
                            },
                        }
                    }
                ]
            }
        },
        {"$project": {"_id": 0, "TA_PROM": {"$avg": "$cstl.sum"}, "EQUIPO": team}},
    ]


def bookings_agg(season, team):
    return [
        {
            "$match": {
                "Season": season,
                "$or": [{"HomeTeam": team}, {"AwayTeam": team}],
                "HY": {"$ne": nan},
                "HR": {"$ne": nan},
                "AY": {"$ne": nan},
                "AR": {"$ne": nan},
            }
        },
        {
            "$facet": {
                "ca": [
                    {
                        "$project": {
                            "_id": 0,
                            "pta": {
                                "$add": [
                                    {
                                        "$cond": {
                                            "if": {"$eq": ["$HomeTeam", team]},
                                            "then": "$HY",
                                            "else": {
                                                "$cond": {
                                                    "if": {"$eq": ["$AwayTeam", team]},
                                                    "then": "$AY",
                                                    "else": 0,
                                                }
                                            },
                                        }
                                    }
                                ]
                            },
                            "ptr": {
                                "$add": [
                                    {
                                        "$cond": {
                                            "if": {"$eq": ["$HomeTeam", team]},
                                            "then": "$HR",
                                            "else": {
                                                "$cond": {
                                                    "if": {"$eq": ["$AwayTeam", team]},
                                                    "then": "$AR",
                                                    "else": 0,
                                                }
                                            },
                                        }
                                    }
                                ]
                            },
                        }
                    }
                ]
            }
        },
        {
            "$project": {
                "_id": 0,
                "A_PROM": {"$sum": [{"$avg": "$ca.pta"}, {"$avg": "$ca.ptr"}]},
                "EQUIPO": team,
            }
        },
    ]
