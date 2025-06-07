" ======================================================================
" Appearance
" ======================================================================
if has('gui_running')
    colorscheme desert
    set lines=999 columns=999
elseif has('mac')
    colorscheme gruvbox
    set background=dark
elseif has('unix')
    colorscheme gruvbox
    set background=dark
else
    colorscheme pablo
endif

" ======================================================================
" Settings appropriate for writing code
" ======================================================================
syntax on            " Turn on syntax highlighting

set autoindent		 " always set autoindenting on
set encoding=utf-8
set expandtab        " expand tabs to spaces
set fileformat=unix  " fileformat = dos or unix
set history=50       " How many lines of history to remember
set nocompatible     " be iMproved, required
set nohlsearch       " Do not highlight search terms
set number           " Set the line number
set shiftwidth=4     " > or < will shift right or left 4 spaces
set showmatch        " Show matching braces, bracket, or parenthesis auto
set softtabstop=4    " tab counts as 4 spaces, not the default 8
set tabstop=4        " tab counts as 4 spaces, not the default 8

" ======================================================================
" Only do this part when compiled with support for autocommands.
" ======================================================================
if has("autocmd")
    " Enable file type detection.
    " Use the default filetype settings, so that mail gets 'tw' set to 72,
    " 'cindent' is on in C files, etc.
    " Also load indent files, to automatically do language-dependent indenting.
    filetype plugin indent on

    " When editing a file, always jump to the last known cursor position.
    " Don't do it when the position is invalid or when inside an event handler
    " (happens when dropping a file on gvim).
    "autocmd BufReadPost *
else
    set autoindent		" always set autoindenting on
endif " has("autocmd")

" ======================================================================
" Change between backslashes and forward slashes
" http://vim.wikia.com/wiki/VimTip431
" \\ to backslash
" \/ to slash
" ======================================================================
"nnoremap <silent> <Leader>/ :let tmp=@/<Bar>s:\\:/:ge<Bar>let @/=tmp<Bar>noh<CR>
"nnoremap <silent> <Leader><Bslash> :let tmp=@/<Bar>s:/:\\:ge<Bar>let @/=tmp<Bar>noh<CR>

" ======================================================================
" Remember last position when reopen a file
" ======================================================================
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" ======================================================================
" Macro
" ======================================================================
let @f = "%afh%"

" ======================================================================
" Custom settings for each file type
" ======================================================================
autocmd BufNewFile *.py 0r ~/my/etc/boy/skel.py
au BufNewFile,BufRead *.py
        \ set tabstop=4
        \ softtabstop=4
        \ shiftwidth=4
        \ expandtab
        \ autoindent
        \ fileformat=unix

autocmd BufNewFile *.rs 0r ~/my/etc/boy/skel.rs

