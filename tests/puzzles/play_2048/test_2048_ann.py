from src.puzzles.ann_2048.ann_2048_trainer import Ann2048Trainer
from src.puzzles.ann_2048.ann_2048_tester import Ann2048Tester

import res.play2048s.anns
import pickle


def open_ann(path=None):
    ann = None
    if not path:
        path = res.play2048s.anns.__path__[0] + "/trained-ann-2048"

    try:
        file = open(path, 'rb')
        ann = pickle.load(file)
        file.close()
    except FileNotFoundError:
        return ann
    print("net loaded")
    return ann


if __name__ == '__main__':

    trainer = Ann2048Trainer(
        structure=[16, 300, 60, 4],
        learning_rate=0.2
    )

    trainer.train(500)
    trainer.save(res.play2048s.anns.__path__[0] + "/trained-ann-")

    tester = Ann2048Tester()
    tester.welch_test()

    for i in range(10, 30):
        trainer = Ann2048Trainer(
            structure=[16, 10 * i, 5 * i, 4],
            learning_rate=0.1
        )

        trainer.train(500)
        trainer.save(res.play2048s.anns.__path__[0] + "/trained-ann-" + i)

        tester = Ann2048Tester()
        tester.welch_test()
