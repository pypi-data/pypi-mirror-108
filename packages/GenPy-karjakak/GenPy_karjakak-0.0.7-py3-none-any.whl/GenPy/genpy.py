# -*- coding: utf-8 -*-
#Copyright (c) 2020, KarjaKAK
#All rights reserved.

import re
from pprint import pprint
import time
import functools
import os

def timer(func):
    """
    Print the runtime of the decorated function
    https://realpython.com/primer-on-python-decorators
    """
    
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"\nFinished {func.__name__!r} in {run_time:.4f} secs\n")
        return(value)    
    return wrapper_timer            

class Fixstr:
    """
    Fixing String Class.
    """
    def __init__(self, text: str):
        self.text = text
        if os.path.isfile(self.text) and self.text.rpartition('.')[2] == 'txt':
            with open(self.text) as rd:
                text = rd.read()
            self.text = text
        self.punc = []
    
    def fixingcom(self, pr: bool = True):
        """Fixing text that has ',' in the middle, which suppose to be punctuated properly. At best!!!"""
        
        return self.prt(',', tuple(sorted((i.group() for i in  tuple(re.finditer(r'\w+\,\w+|\w+\,  \w+', self.text)) if len(i.group().rpartition(',')[2]) >= 1 and any([i.group().rpartition(',')[2].istitle(), i.group().rpartition(',')[2].islower()])  and len(i.group().rpartition(',')[0]) > 1), key = lambda k: k.partition(',')[2])), pr)
    
    def fixingdc(self, pr: bool = True):
        """Fixing text that has ';' in the middle, which suppose to be punctuated properly. At best!!!"""
        
        return self.prt(';', tuple(sorted((i.group() for i in  tuple(re.finditer(r'\w+\;\w+|\w+\;  \w+', self.text)) if len(i.group().rpartition(';')[2]) >= 1 and any([i.group().rpartition(';')[2].istitle(), i.group().rpartition(';')[2].islower()])  and len(i.group().rpartition(';')[0]) > 1), key = lambda k: k.partition(';')[2])), pr)
        
    def fixingdd(self, pr: bool = True):
        """Fixing text that has ':' in the middle, which suppose to be punctuated properly. At best!!!"""
        
        return self.prt(':', tuple(sorted((i.group() for i in  tuple(re.finditer(r'\w+\:\w+|\w+\:  \w+', self.text)) if len(i.group().rpartition(':')[2]) >= 1 and any([i.group().rpartition(':')[2].istitle(), i.group().rpartition(':')[2].islower()])  and len(i.group().rpartition(':')[0]) > 1), key = lambda k: k.partition(':')[2])), pr)
        
    def fixingfs(self, pr: bool = True):
        """Fixing text that has '.' in the middle, which suppose to be punctuated properly. At best!!!"""
        
        return self.prt('.', tuple(sorted((i.group() for i in  tuple(re.finditer(r'\w+\.\w+|\w+\.  \w+', self.text)) if len(i.group().rpartition('.')[2]) >= 1 and i.group().rpartition('.')[2].istitle() and len(i.group().rpartition('.')[0]) > 1), key = lambda k: k.partition('.')[2])), pr)
    
    #Supposed to stand alone for the fact that so many familiarity.#
    def fixingpar(self, pr: bool = True):
        """Fixing text that has '\n' in the middle, which suppose to be punctuated properly. At best!!!"""
        
        return self.prt('\n', tuple(sorted((i.group() for i in  tuple(re.finditer(r'\w+\S?\s?\S+?\n\S?\w+', self.text)) if len(i.group().rpartition('\n')[2]) >= 1 and any([i.group().rpartition('\n')[2].istitle(), i.group().rpartition('\n')[2].islower(), i.group().rpartition('\n')[2].isupper()]) and len(i.group().rpartition('\n')[0]) > 1), key = lambda k: k.partition('\n')[2])), pr)    
    
    def prt(self, punc: str, mini: dict, pr: bool) -> str:
        """Printing and result of the string"""
        
        if pr:
            print(f'Fixes needed for {repr(punc)}!')
            pprint(mini)
            print(f'Total faults: {len(mini)}\n\nFinished fixes:')
        for w in mini:
            if punc == '\n':
                if any([w.partition('\n')[0][-1].isalpha(), w.partition('\n')[0][-1].isnumeric(), w.partition('\n')[0][-1] in [',', ';']]) and w.partition('\n')[2].islower():
                    a = w.replace(f'{punc}', f' ')
                elif w.partition('\n')[0][-1] in ['.', ':'] and w.partition('\n')[2].islower():
                    a = ''.join(w.partition('\n')[:2]) + w.partition('\n')[2].title()
                    a = a.replace(f'{punc}', f'{punc}{punc}')
                else:
                    a = w.replace(f'{punc}', f'{punc}{punc}')
            else:
                a = w.replace(f'{punc} ', f'{punc}') if w.partition(f'{punc}')[2][:2].isspace() else w.replace(f'{punc}', f'{punc} ')
            if pr: print(f'{w} => {a}')
            self.text = f'{self.text[:self.text.find(w)]}{a}{self.text[self.text.find(w) + len(w):]}'
            del a, w
        del mini, punc
        if pr: print('\n')
        return self.text
    
    @timer
    def fixingall(self, pr: bool = True) -> str:
        """Fixing text that has ['.', ',', ';', ':', '\n'] in the middle, which suppose to be punctuated properly. At best!!!"""
        
        for fixing in (self.fixingfs, self.fixingcom, self.fixingdc, self.fixingdd, self.fixingpar):
            self.text = fixing(pr)
        return self.text
    
    def savefix(self, filename: str):
        """Saving Fixed string to a new file."""
        
        if not os.path.isfile(filename):
            fx = self.fixingall(False)
            with open(filename := filename if filename.rpartition('.')[2] == 'txt' else f'{filename}.txt', 'w') as tx:
                tx.write(fx)
            del fx
        else:
            raise Exception('This file is already exist, please create new one!!!')