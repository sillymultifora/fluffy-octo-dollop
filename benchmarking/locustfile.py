from locust import HttpUser, task, between


class LLMUser(HttpUser):
    wait_time = between(3, 10)

    @task(1)
    def short_sequence(self):
        self.client.post("/process", json={"input": "What is the capital of France?"})

    @task(1)
    def medium_sequence(self):
        self.client.post(
            "/process",
            json={
                "input": "Who wrote the novel Pride and Prejudice and in what year was it first published?"
            },
        )

    @task(1)
    def long_sequence(self):
        self.client.post(
            "/process",
            json={
                "input": "Explain the process of photosynthesis in plants, highlighting the role of chlorophyll, sunlight, carbon dioxide, and water in producing glucose and oxygen."
            },
        )

    @task(1)
    def very_long_sequence(self):
        story_prompt = (
            "Once upon a time in a distant kingdom, a brave knight set out on a perilous journey to rescue "
            "the princess from the clutches of a fearsome dragon. After days of traveling through dense forests "
            "and crossing treacherous rivers, he finally reached the dragon’s lair..."
        )
        self.client.post("/process", json={"input": story_prompt})

    @task(1)
    def extremely_long_sequence(self):
        passage = (
            "The Great Barrier Reef, located off the coast of Queensland, Australia, is the largest coral reef "
            "system in the world, stretching over 2,300 kilometers and covering an area of approximately 344,400 square "
            "kilometers. It is composed of over 2,900 individual reefs and 900 islands, and supports a wide variety "
            "of marine life. The reef has become one of the most complex ecosystems on the planet, but it is under threat "
            "from climate change, overfishing, and pollution. Efforts to conserve the reef are ongoing, but its future "
            "remains uncertain."
        )
        self.client.post("/process", json={"input": passage})
