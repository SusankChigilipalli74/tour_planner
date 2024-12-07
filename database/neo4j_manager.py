from neo4j import GraphDatabase
from config.config import settings

class Neo4jManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def create_user_node(self, user_id: str, preferences: dict):
        with self.driver.session() as session:
            session.run(
                """
                MERGE (u:User {user_id: $user_id})
                SET u += $preferences
                """,
                user_id=user_id,
                preferences=preferences
            )

    def update_user_preferences(self, user_id: str, preferences: dict):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:User {user_id: $user_id})
                SET u += $preferences
                """,
                user_id=user_id,
                preferences=preferences
            )

    def create_visit_relationship(self, user_id: str, place: str, sentiment: str):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u:User {user_id: $user_id})
                MERGE (p:Place {name: $place})
                CREATE (u)-[:VISITED {sentiment: $sentiment}]->(p)
                """,
                user_id=user_id,
                place=place,
                sentiment=sentiment
            )