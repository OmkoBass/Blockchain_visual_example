import hashlib
import json
import pygame
from time import time
from random import choice, randint

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="SATOSHI NAKAMOTO, FREEDOM & LIBERTY", proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'receiver': recipient,
            'score': amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash


def contestants_transaction():
    global names
    global blockchain
    global blocks
    global max_blocks

    # I don't want to constantly add blocks
    if blocks <= max_blocks:
        # Chooses random names from a list
        first_random_contestant = choice(names)
        second_random_contestant = choice(names)
        gift_score = randint(0, 100)

        blockchain.new_transaction(first_random_contestant, second_random_contestant, gift_score)

        new_block = randint(0, 99999)
        blockchain.new_block(new_block)

        blocks += 1


def draw_blocks():
    i = 0
    j = 0
    for block in blockchain.chain:
        # I keep track of i and j
        # for displaying a matrix of blocks
        if i == blocks_per_row:
            j += 1
            i = 0
        
        # If there's no transactions in the block
        # then just show No transactions
        if not block['transactions']:
            pygame.draw.rect(screen, COLOR_WHITE, pygame.Rect(i * OFFSET + PADDING_OFFSET, j * OFFSET + PADDING_OFFSET, BLOCK_SIZE, BLOCK_SIZE))
            label = font.render("No transactions", 1, COLOR_BLACK)
            screen.blit(label, (i * OFFSET + PADDING_OFFSET, j * OFFSET + (BLOCK_SIZE / 3) + PADDING_OFFSET))

        # For each transaction in a block
        # draw a rectangle and it's content
        for transaction in block['transactions']:
            if transaction:
                sender = transaction['sender']
                reciever = transaction['receiver']
                score = transaction['score']

                rectangle_color = COLOR_WHITE
                text_color = COLOR_BLACK

                if sender == 'Lucifer' or reciever == 'Lucifer':
                    rectangle_color = COLOR_RED
                    text_color = COLOR_WHITE
                elif sender == 'Pythagoras' or reciever == 'Pythagoras':
                    rectangle_color = COLOR_BLUE
                    text_color = COLOR_WHITE
                elif sender == 'Barney' or reciever == 'Barney':
                    rectangle_color = COLOR_YELLOW
                elif sender == 'Baron' or reciever == 'Baron':
                    rectangle_color = COLOR_DARK_RED
                    text_color = COLOR_WHITE

                pygame.draw.rect(screen, rectangle_color, pygame.Rect(i * OFFSET + PADDING_OFFSET, j * OFFSET + PADDING_OFFSET, BLOCK_SIZE, BLOCK_SIZE))

                label_sender = font.render(f'Sender: {sender}', 1, text_color)
                screen.blit(label_sender, (i * OFFSET + PADDING_OFFSET, j * OFFSET + (BLOCK_SIZE / 3) + PADDING_OFFSET))

                label_reciever = font.render(f'Reciever: {reciever}', 1, text_color)
                screen.blit(label_reciever, (i * OFFSET + PADDING_OFFSET, j * OFFSET + 20 + (BLOCK_SIZE / 3) + PADDING_OFFSET))

                label_score = font.render(f'Score: {score}', 1, text_color)
                screen.blit(label_score, (i * OFFSET + PADDING_OFFSET, j * OFFSET + 40 + (BLOCK_SIZE / 3) + PADDING_OFFSET))
        i += 1


names = [
        "Jack",
        "Baron",
        "Aimee",
        "Duke",
        "Chad",
        "Tatiana",
        "Lesley",
        "Freedom",
        "Liberty",
        "Barney",
        "Deimos",
        "Achilles",
        "Marcus",
        "Plato",
        "Pythagoras",
        "Lucifer",
        "Brut",
    ]

# Current number of blocks
blocks = 0

# Maximum number of blocks
max_blocks = 18

# How many blocks per row should there be
blocks_per_row = 5

# Sizes
BLOCK_SIZE = 160
SCREEN_SIZE_WIDTH = 900
SCREEN_SIZE_HEIGHT = 720

OFFSET = 180

# For the UI to be centered
PADDING_OFFSET = 10

blockchain = Blockchain()

# Defined color hex
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_DARK_RED = (139,0,0)

pygame.init()
pygame.display.set_caption("Blockchain")

font = pygame.font.SysFont("monospace", 13)
screen = pygame.display.set_mode((SCREEN_SIZE_WIDTH, SCREEN_SIZE_HEIGHT))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    contestants_transaction()

    draw_blocks()
    pygame.display.update()
