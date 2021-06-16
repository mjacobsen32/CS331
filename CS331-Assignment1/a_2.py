import sys

class State:
    def __init__(s,parent,lc,lw,lb,rc,rw,rb,d):
        s.depth = d
        s.parent = parent
        s.lc = lc
        s.lw = lw
        s.lb = lb
        s.rc = rc
        s.rw = rw
        s.rb = rb
    def state_allowed(s, lc, lw, lb, rc, rw, rb):
        if (lc < lw and lc > 0) or (rc < rw and rc > 0):
            return False
        if lc < 0 or lw < 0 or rc < 0 or rw < 0:
            return False
        else:
            return True
    def one_chick(s):
        if s.lb == 1:
            if s.state_allowed(s.lc-1,s.lw,0,s.rc+1,s.rw,1):
                new = State(s,s.lc-1,s.lw,0,s.rc+1,s.rw,1,s.depth+1)
                return(new)
        elif s.rb == 1:
            if s.state_allowed(s.lc+1,s.lw,1,s.rc-1,s.rw,0):
                new = State(s,s.lc+1,s.lw,1,s.rc-1,s.rw,0,s.depth+1)
                return(new)
        return(0)
    def two_chick(s):
        if s.lb == 1:
            if s.state_allowed(s.lc-2,s.lw,0,s.rc+2,s.rw,1):
                new = State(s,s.lc-2,s.lw,0,s.rc+2,s.rw,1,s.depth+1)
                return(new)
        elif s.rb == 1:
            if s.state_allowed(s.lc+2,s.lw,1,s.rc-2,s.rw,0):
                new = State(s,s.lc+2,s.lw,1,s.rc-2,s.rw,0,s.depth+1)
                return(new)
        return(0)
    def one_wolf(s):
        if s.lb == 1:
            if s.state_allowed(s.lc,s.lw-1,0,s.rc,s.rw+1,1):
                new = State(s,s.lc,s.lw-1,0,s.rc,s.rw+1,1,s.depth+1)
                return(new)
        elif s.rb == 1:
            if s.state_allowed(s.lc,s.lw+1,1,s.rc,s.rw-1,0):
                new = State(s,s.lc,s.lw+1,1,s.rc,s.rw-1,0,s.depth+1)
                return(new)
        return(0)
    def two_wolf(s):
        if s.lb == 1:
            if s.state_allowed(s.lc,s.lw-2,0,s.rc,s.rw+2,1):
                new = State(s,s.lc,s.lw-2,0,s.rc,s.rw+2,1,s.depth+1)
                return(new)
        elif s.rb == 1:
            if s.state_allowed(s.lc,s.lw+2,1,s.rc,s.rw-2,0):
                new = State(s,s.lc,s.lw+2,1,s.rc,s.rw-2,0,s.depth+1)
                return(new)
        return(0)
    def one_chick_one_wolf(s):
        if s.lb == 1:
            if s.state_allowed(s.lc-1,s.lw-1,0,s.rc+1,s.rw+1,1):
                new = State(s,s.lc-1,s.lw-1,0,s.rc+1,s.rw+1,1,s.depth+1)
                return(new)
        elif s.rb == 1:
            if s.state_allowed(s.lc+1,s.lw+1,1,s.rc-1,s.rw-1,0):
                new = State(s,s.lc+1,s.lw+1,1,s.rc-1,s.rw-1,0,s.depth+1)
                return(new)
        return(0)
    def print_state(s):
        print(str(s.lc) + ',' + str(s.lw) + ',' + str(s.lb) + ',' + str(s.rc)+ ',' + str(s.rw)+ ',' + str(s.rb))
    def get_string(s):
        return(str(s.lc) + ',' + str(s.lw) + ',' + str(s.lb) + ',' + str(s.rc)+ ',' + str(s.rw)+ ',' + str(s.rb))

class Problem:
    def __init__(river_obj, initial_state_file, goal_state_file, mode, output_file,max_d):
        river_obj.moves = 0
        river_obj.max_depth = 100
        river_obj.curr_max_depth = max_d
        river_obj.explored = []
        river_obj.mode = mode
        river_obj.output_file = output_file

        initial_arr = []
        with open(initial_state_file) as initial:
            for line in initial:
                initial_arr += line.strip().split(',')
        river_obj.current = State(0,int(initial_arr[0]),int(initial_arr[1]),int(initial_arr[2]),int(initial_arr[3]),int(initial_arr[4]),int(initial_arr[5]),0)
        river_obj.frontier = [river_obj.current]
        final_arr = []
        with open(goal_state_file) as final:
            for line in final:
                final_arr += line.strip().split(',')
        river_obj.final = State(-1,int(final_arr[0]),int(final_arr[1]),int(final_arr[2]),int(final_arr[3]),int(final_arr[4]),int(final_arr[5]),-1)
    def print_impossible(riv):
        if riv.mode == 'dfs' or riv.mode == 'bfs' or riv.mode == 'astar':
            print("no solution found")
    def empty_frontier(r):
        if len(r.frontier) == 0: return True
        else: return False
    def next_node(r):
        r.current = r.frontier.pop(0)
    def complete(r):
        if  ((r.current.lc == r.final.lc) and
            (r.current.lw == r.final.lw) and
            (r.current.lb == r.final.lb)  and
            (r.current.rc == r.final.rc) and
            (r.current.rw == r.final.rw) and
            (r.current.rb == r.final.rb)):
            return(True)
        else:
            return(False)
    def print_screen(r):
        l = []
        parent = r.current.parent
        while parent != 0:
            l.append(parent.get_string())
            parent = parent.parent
        l.reverse()
        sys.stdout = open(riv.output_file, 'w')
        for i in l:
            print(i)
        print(r.final.get_string())
        print("Nodes expanded: " + str(r.moves))
        print("Path Length: " + str(len(l)))
        sys.stdout.close()
        with open(riv.output_file, 'r') as f:
            contents = f.read()
        sys.stdout = sys.__stdout__
        print(contents)
    def add_explored(r):
        r.explored.append(r.current)
    def states_equal(r,s1,s2):
        if (s1.lc == s2.lc and
            s1.lw == s2.lw and
            s1.lb == s2.lb and
            s1.rc == s2.rc and
            s1.rw == s2.rw and
            s1.rb == s2.rb):
            return True
        else:
            return False
    def not_in_frontier(r,s):
        for i in r.frontier:
            if r.states_equal(s,i):
                return(False)
        return(True)
    def not_in_explored(r,s):
        for i in r.explored:
            if r.states_equal(s,i):
                return(False)
        return(True)
    def add_to_frontier(r,s):
        if r.mode == "dfs":
            r.frontier.insert(0,s)
        elif r.mode == "bfs":
            r.frontier.append(s)
        elif r.mode == 'iddfs':
            r.frontier.insert(0,s)
        elif r.mode == 'astar':
            count = 0
            placed = False
            for i in r.frontier:
                if r.h(s) < r.h(i):
                    r.frontier.insert(count,s)
                    placed = True
                    break
                count+=1
            if placed == False:
                r.frontier.append(s)
    def not_passed_max(r,s):
        if r.mode == 'dfs' or r.mode == 'bfs' or r.mode == 'astar':
            return(True)  
        elif r.mode == 'iddfs':
            if s.depth < r.curr_max_depth:
                return(True)
            else:
                return(False)   
    def expand(r):
        child = r.current.one_chick()
        if child != 0:
            if r.not_in_explored(child) and r.not_in_frontier(child) and r.not_passed_max(child):
                r.add_to_frontier(child)
        child = r.current.two_chick()
        if child != 0:
            if r.not_in_explored(child) and r.not_in_frontier(child) and r.not_passed_max(child):
                r.add_to_frontier(child)
        child = r.current.one_wolf()
        if child != 0:
            if r.not_in_explored(child) and r.not_in_frontier(child) and r.not_passed_max(child):
                r.add_to_frontier(child)
        child = r.current.one_chick_one_wolf()
        if child != 0:
            if r.not_in_explored(child) and r.not_in_frontier(child) and r.not_passed_max(child):
                r.add_to_frontier(child)
        child = r.current.two_wolf()
        if child != 0:
            if r.not_in_explored(child) and r.not_in_frontier(child) and r.not_passed_max(child):
                r.add_to_frontier(child)
    def print_frontier(r):
        for i in r.frontier:
            i.print_state()
    def print_explored(r):
        for i in r.explored:
            i.print_state()       
    def h(r,s):
        if r.final.lb == 1:
            return(abs(r.final.lc - s.lc) + abs(r.final.lw - s.lw))
        elif r.final.rb == 1:
            return(abs(r.final.rc - s.rc) + abs(r.final.rw - s.rw))

riv = Problem(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],1)

go = True
m = 1000

counter = 2
c = True
found = False
while c == True:
    go = True
    while go == True:
        if riv.empty_frontier() == True:
            riv.print_impossible()
            go = False
            break
        riv.next_node()
        if riv.complete() == True:
            riv.print_screen()
            go = False
            c = False
            found = True
            break
        riv.add_explored()
        riv.expand()
        riv.moves+=1
    if riv.mode == 'dfs' or riv.mode == 'bfs' or riv.mode == 'astar':
        c = False
    elif riv.mode == 'iddfs':
        if counter > m:
            c = False
        else:
            riv = Problem(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],counter)
            counter+=1
    if counter == m and found == fale:
        print("no solution found")