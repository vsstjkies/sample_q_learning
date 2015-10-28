# coding:utf-8

import random

# デバッグ用標準出力
def debug_print(obj_message):
    # print obj_message
    pass


gamma = 0.99 # 割引率 0＜γ≦1
alpha = 01 # 学習係数 0＜α≦1

class Agent:

    def __init__(self):

        self.states_count = 5 # 状態は5つ
        self.states = [] # 状態S
        for var in range(0, self.states_count):
            action = {
                'left':random.random(), # Q値を擬似乱数（0~1の浮動小数点数）で初期化
                'right':random.random()
            }
            self.states.append( action ) # 状態に行動をネスト
        self.time = 0 # 時間t（行動回数）
        self.current_state_num = 0
        self.actions = []



    def act(self): # 行動

        debug_print('time : ' + str(self.time) )
        self.policy()
        
        action = self.actions[-1] # リスト配列の末，つまり最後の要素を取得する

        one_before_state_num = self.current_state_num
        
        self.time = self.time + 1
        if action is 'right':
            self.current_state_num = self.current_state_num + 1
        elif action is 'left':
            self.current_state_num = self.current_state_num + 0
        else:
            print 'error : act()'

        # 以下，Q値の再計算
        old_q = self.states[ one_before_state_num ][action]

        # 選択肢の中で最も高いQ値を取得
        max_q = None
        next_right_q = self.states[ self.current_state_num ]['right']
        next_left_q = self.states[ self.current_state_num ]['left']
        if next_left_q < next_right_q:
            max_q = next_right_q
        else:
            max_q = next_left_q

        reward = self.get_reward() # 報酬

        # Qの値を再計算
        new_q = old_q + alpha * (
            reward + gamma * max_q - old_q
            )

        self.states[ one_before_state_num ][ action ] = new_q
        
        if reward is 1: # ゴールに到着している場合は最初の位置に戻す
            self.current_state_num = 0
         

    def policy(self): # 方策（左に進むか，右に進むかを決める）

        is_left_end = self.current_state_num is 0
        is_right_end = self.current_state_num is self.states_count - 1
        if is_left_end:
            debug_print('左端にいるから→')
            self.actions.append('right')
        elif is_right_end:
            debug_print('右端にいるから←')
            self.actions.append('left')
        else:
            # 今回はε-greedy法で方策として採用する
            debug_print('ε-greedy法')
            self.epsilon_greedy_algorithm()



    def epsilon_greedy_algorithm(self):
        # 一定の確率εで、或る環境sから取り得る行動のうち一つをランダムに選び、
        # 1-εの確率で或る環境sから最大のQ値を持つ行動aを選択する

        epsilon = random.randint(0, 1) # 0 <= N <= 1 なランダムな整数 N

        if epsilon: # ランダムで行動を選択
            left_or_right = random.randint(0, 1)
            if left_or_right:
                debug_print('ランダムに→')
                self.actions.append('right')
            else:
                debug_print('ランダムに←')
                self.actions.append('left')
        else: # 最大のQ値を持つ行動を選択
            left_q_val = self.states[ self.current_state_num ]['left']
            right_q_val = self.states[ self.current_state_num ]['right']
            if left_q_val < right_q_val:
                debug_print( str(left_q_val)  + ' < ' + str(right_q_val) )
                debug_print('Q値の高い方を選択して→')
                self.actions.append('right')
            else:
                debug_print( str(left_q_val)  + ' > ' + str(right_q_val) )
                debug_print('Q値の高い方を選択して←')
                self.actions.append('left')



    def get_reward(self):

        # ゴールに到着している場合のみ報酬を与える
        if self.current_state_num is self.states_count - 1:
            return 1
        else:
            return 0

        

    # Q値を出力
    def print_q_val(self):

        for state in self.states:
            print state['left']
            print state['right']
            print



    # エージェントが環境中のどの位置に居るか視覚的に出力
    def print_localtion(self):

        location_string = ''
        for val in range(0, self.states_count):
            if self.current_state_num is val:
                location_string = location_string + '●'
            else:
                location_string = location_string + '○'
        print location_string




agent = Agent()
agent.print_q_val()
# while True:
for val in range(0, 1000):
    agent.act()
    agent.print_localtion()
    # raw_input() # 処理を止めてコマンドラインを確認する

agent.print_q_val()

    
