from angle_emb import AnglE, Prompts


def embed(txt):
    angle = AnglE.from_pretrained('WhereIsAI/UAE-Large-V1',
                                  pooling_strategy='cls')
    angle.set_prompt(prompt=Prompts.C)
    return angle.encode({'text': txt}, to_numpy=True)


if __name__ == "__main__":
    print(embed("Hello, World!!!"))
