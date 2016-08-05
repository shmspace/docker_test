set nocompatible               " be iMproved
filetype off                   " required!    

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required! 
"这是vundle本身的设置
Bundle 'gmarik/vundle'  
 
" My Bundles here:
" 这里是设置你自己自定义的插件的设置vundle设置，注意：下载的插件git为：https://github.com/godlygeek/tabular.git，则设置为Bundle 'godlygeek/tabular';https://github.com/gmarik/vundle.git设置则为 Bundle 'gmarik/vundle'  
" original repos on github
Bundle 'godlygeek/tabular'

" vim-scripts repos，vim-scripts的访问地址，格式则如下：
Bundle 'L9'
Bundle 'FuzzyFinder'
" 字节对齐
Plugin 'matchit.zip'
" 代码折叠
Plugin 'tmhedberg/SimpylFold'
" 缩进插件
Plugin 'vim-scripts/indentpython.vim'
" 自动补全
Bundle 'Valloric/YouCompleteMe'
" 语法高亮
Plugin 'scrooloose/syntastic'
" PEP8代码风格检查
Plugin 'nvie/vim-flake8'
" 文件树
Plugin 'scrooloose/nerdtree'
" 使用tab键
Plugin 'jistr/vim-nerdtree-tabs'
" non github repos ，非git的访问地址的，格式如下：
Bundle 'git://git.winicent.com/command-t.git'
" ...

filetype plugin indent on     " required!
"
" Brief help
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install(update) bundles
" :BundleSearch(!) foo - search(or refresh cache first) for foo
" :BundleClean(!)      - confirm(or auto-approve) removal of unused bundles
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle command are not allowed..
"
" 切分窗口及切换窗口配置
set splitbelow
set splitright

"split navigations
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" 折叠代码块配置
" Enable folding
set foldmethod=indent
set foldlevel=99

" Enable folding with the spacebar
nnoremap <space> za

let g:SimpylFold_docstring_preview=1

" 缩进配置
au BufNewFile,BufRead *.py
\ set tabstop=4 |
\ set softtabstop=4 |
\ set shiftwidth=4 |
\ set textwidth=179 |
\ set expandtab |
\ set autoindent |
\ set fileformat=unix

au BufNewFile,BufRead *.js, *.html, *.css
\ set tabstop=2 |
\ set softtabstop=2 |
\ set shiftwidth=2
    
" 标示不必要的空格
highlight WhitespaceEOL guibg=red 
match WhitespaceEOL /\s\+$/
set list " 显示特殊符号
set listchars=tab:›\ ,trail:•,extends:>,precedes:<,nbsp:.

" 设置高亮搜寻
set hls

" 补全设置
let g:ycm_python_binary_path = 'python'
let g:ycm_autoclose_preview_window_after_completion=1
map <leader>g:YcmCompleter GoToDefinitionElseDeclaration<CR>

" 代码风格检查
let python_highlight_all=1
syntax on

" 隐藏pyc文件
let NERDTreeIgnore=['\.pyc$', '\~$'] "ignore files in NERDTree

" tab换为2个控制
set ts=2
set expandtab

" 配色方案
colorscheme candy
" 显示行号
set number
