
import os
import openai
from settings import *

openai.api_key = os.getenv('OPENAI_KEY')

def chat(input, prompt):
	prompt += 'You: ' + input
	answer, prompt = gpt3(prompt,
							engine='text-davinci-002',
							response_length=30,
							temperature=0.9,
							top_p=1,
							frequency_penalty=0,
							presence_penalty=0.6,
							start_text='\nBartender:',
							restart_text='\nYou: ',
							stop_seq=['\nYou:', '\nBartender:' '\n'])
	print('GPT-3:' + answer)
	return answer, prompt

def gpt3(prompt, engine='davinci', response_length=64,
         temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0,
         start_text='', restart_text='', stop_seq=[]):
    response = openai.Completion.create(
        prompt=prompt + start_text,
        engine=engine,
        max_tokens=response_length,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop_seq,
    )
    answer = response.choices[0]['text']
    new_prompt = prompt + start_text + answer + restart_text
    return answer, new_prompt

class Chat():
	def __init__(self, game):
		self.box_size = (WIDTH / 2, HEIGHT / 3)
		self.box_posx = WIDTH / 4
		self.box_posy = HEIGHT /3
		self.chat_box = pg.Surface(self.box_size).convert_alpha()
		self.chat_box2 = pg.Surface((WIDTH / 2 + 20, HEIGHT / 3 + 20)).convert_alpha()
		self.chat_box3 = pg.Surface((pg.transform.scale2x(game.npc_img).get_size())).convert_alpha()
		self.chat_box.fill((200,200,200))
		self.chat_box2.fill((200,200,200))
		self.chat_box3.fill((100,100,100))
		self.answer = "Hey Cowboy! I need your help!"
		self.prompt = TRAINING_DATA
		self.font = pg.font.Font(None, 32)
		self.input_box = pg.Rect(self.box_posx, 
								self.box_posy + (self.chat_box.get_height()) - 32, 
								self.chat_box.get_width(), 32)
		self.color = pg.Color('dodgerblue2')
		self.text = ''
		self.done = False

	def refresh_chat(self, game):
		game.screen.blit(self.chat_box2, (self.box_posx - 10, self.box_posy - 10))
		game.screen.blit(self.chat_box, (self.box_posx, self.box_posy))
		game.screen.blit(self.chat_box3, (self.box_posx, self.box_posy))
		game.screen.blit(pg.transform.scale2x(game.npc_img), (self.box_posx - 7, self.box_posy - 3))
		game.draw_text("HENRY", game.text_font, 50, RED, self.box_posx + 120, self.box_posy, align="nw")
		game.draw_text("Press ESC to quit", game.text_font, 20, RED, 
						self.box_posx + self.chat_box.get_width(), self.box_posy, align="ne")

	def chat_screen(self, game):
		game.screen.blit(game.dim_screen, (0, 0))
		self.refresh_chat(game)
		while not self.done:
			for event in pg.event.get():
				if event.type == pg.KEYUP:
					if event.key == pg.K_ESCAPE:
						game.chat = not game.chat
						self.done = True
				if event.type == pg.KEYUP:
					if event.key == pg.K_RETURN:
						print(self.text)
						self.answer, self.prompt = chat(self.text, self.prompt)
						self.text = ''
						self.refresh_chat(game)
					elif event.key == pg.K_BACKSPACE:
						self.text = self.text[:-1]
					else:
						self.text += event.unicode

		# Render the current text.
			txt_surface = self.font.render(self.text, True, self.color)
		# Resize the box if the text is too long.
			width = max(self.chat_box.get_width(), txt_surface.get_width()+10)
			self.input_box.w = width
			box_fill = pg.Surface((width, 32))
			box_fill.fill(WHITE)
		# Blit the text.
			game.screen.blit(box_fill, self.input_box)
			txt_posx = self.input_box.centerx - (txt_surface.get_width() / 2)
			game.screen.blit(txt_surface, (txt_posx, self.input_box.y+5))
		# Blit the input_box rect.
			pg.draw.rect(game.screen, self.color, self.input_box, 2)
		# Ajust the answer if text is too long
			n = 10
			answer_part = self.answer.split()
			answer_part = [' '.join(answer_part[i:i+n]) for i in range(0,len(answer_part),n)]
			i = 0
			for part in answer_part:
				i += 50
				game.draw_text(part, game.text_font, 50, BLACK,
								self.box_posx + (self.chat_box.get_width() // 2) , 
								self.box_posy + (self.chat_box.get_height() // 3) + i - 50, 
								align="center")
			pg.display.flip()
