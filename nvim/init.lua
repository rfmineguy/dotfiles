require ("rf")

vim.opt.number = true
vim.opt.mouse = 'a'
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.hlsearch = false
vim.opt.wrap = true
vim.opt.breakindent = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = false
vim.opt.relativenumber = true
vim.opt.foldmethod = "expr"
vim.opt.foldexpr = "nvim_treesitter#foldexpr()"
vim.cmd([[ set nofoldenable ]])
vim.cmd([[ au BufRead,BufNewFile *.s set filetype=kickass ]])
vim.cmd([[ au BufRead,BufNewFile *.ejs set filetype=html ]])

vim.filetype.add({
	pattern = {
		["*.s"] = "kickass"
	},
})

--
-- select all text in file
--
vim.keymap.set('n', '<leader>a', ':keepjumps normal! ggVG<cr>')

--
-- plugin manager
--
local lazy = {}

function lazy.install(path)
  if not vim.loop.fs_stat(path) then
    print('Installing lazy.nvim....')
    vim.fn.system({
      'git',
      'clone',
      '--filter=blob:none',
      'https://github.com/folke/lazy.nvim.git',
      '--branch=stable', -- latest stable release
      path,
    })
  end
end

function lazy.setup(plugins)
  if vim.g.plugins_ready then
    return
  end

  -- You can "comment out" the line below after lazy.nvim is installed
  lazy.install(lazy.path)

  vim.opt.rtp:prepend(lazy.path)

  require('lazy').setup(plugins, lazy.opts)
  vim.g.plugins_ready = true
end

lazy.path = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
print(lazy.path)
lazy.opts = {}
lazy.setup({
	-- Plugins here
	-- { 'christoomey/vim-tmux-navigator' },
	{ 'folke/tokyonight.nvim' },
	{ 'nvim-lua/plenary.nvim' },
	{ 'LinArcX/telescope-command-palette.nvim' },
-- or                              , branch = '0.1.x','}
	{ 'lukas-reineke/indent-blankline.nvim', main = 'ibl', opts = {} },
	{ 'catppuccin/nvim', name = 'catppuccin', priority = 1000 },
	{ 'nvim-treesitter/nvim-treesitter', build = ':TSUpdate' },
	{ 'nvim-treesitter/playground' },
	{ 'tpope/vim-fugitive' },
	-- LSP stuff
  { 'VonHeikemen/lsp-zero.nvim', branch = 'v3.x' },
  { 'neovim/nvim-lspconfig' },
  { 'hrsh7th/cmp-nvim-lsp' },
  { 'hrsh7th/nvim-cmp', event = { "InsertEnter", "CmdlineEnter" } },
	{ 'williamboman/mason.nvim' },
	{ 'williamboman/mason-lspconfig.nvim' },
	{ 'Civitasv/cmake-tools.nvim' },
	{ 'L3MON4D3/LuaSnip', version = "v2.*", build = "make install_jsregexp", dependencies = { "rafamadriz/friendly-snippets" }},
	-- Git
	{ 'NeogitOrg/neogit', dependencies = { "sindrets/diffview.nvim" }, config = true },
	-- Haskell
	{
		'mrcjkb/haskell-tools.nvim',
		version = '^3', -- Recommended
		ft = { 'haskell', 'lhaskell', 'cabal', 'cabalproject' },
	},
	{ 'saadparwaiz1/cmp_luasnip' },
	-- { 'mfussenegger/nvim-dap',
	-- 	config = function()
	-- 		local dap = require("dap")
	-- 		dap.adapters.lldb = {
	-- 			type = 'executable',
	-- 			command = '/opt/homebrew/Cellar/llvm/17.0.6_1/bin/lldb-vscode',
	-- 			name = 'lldb'
	-- 		}
	-- 		dap.configurations.cpp = {
	-- 			{
	-- 				type = 'lldb',
	-- 				name = 'Launch',
	-- 				request = 'launch',
	-- 				program = function()
	-- 					return vim.fn.input('Path to executable: ', vim.fn.getcwd()..'/', 'file')
	-- 				end,
	-- 				cwd = '${workspaceFolder}',
	-- 				terminal = 'integrated',
	-- 				stopOnEntry = false,
	-- 				args = {}
	-- 			}
	-- 		}
	-- 		dap.configurations.c = dap.configurations.cpp
	-- 		dap.configurations.rust = dap.configurations.cpp

	-- 		vim.keymap.set('v', '<leader>db', dap.toggle_breakpoint, {silent=true})
	-- 		vim.keymap.set('v', '<F10>', dap.step_over, {silent=true})
	-- 		vim.keymap.set('v', '<F11>', dap.step_into, {silent=true})
	-- 	end
	-- },
	-- { 'theHamsta/nvim-dap-virtual-text' },
	-- { "rcarriga/nvim-dap-ui", dependencies = {"mfussenegger/nvim-dap", "nvim-neotest/nvim-nio"},
	-- 	config = function ()
	-- 		require('dapui').setup()
	-- 		local dap, dapui = require('dap'), require('dapui')
	-- 		dap.listeners.before.attach.dapui_config = function ()
	-- 			dapui.open()
	-- 		end
	-- 		dap.listeners.before.launch.dapui_config = function()
	-- 			dapui.open()
	-- 		end
	-- 		dap.listeners.before.event_terminated.dapui_config = function()
	-- 			dapui.close()
	-- 		end
	-- 		dap.listeners.before.event_exited.dapui_config = function()
	-- 			dapui.close()
	-- 		end
	-- 		-- vim.keymap.set('v', '<leader>de', dapui.expand())
	-- 	end
	-- },
	{ 'nvim-telescope/telescope.nvim', tag = '0.1.5' },
	{ 'nvim-telescope/telescope-dap.nvim' },
	{ "folke/neodev.nvim", opts = {},
		config = function()
			require("neodev").setup({
				library = { plugins = { "nvim-dap-ui" }, types = true }
			})
		end
	},
	{ 'ryanoasis/vim-devicons' }
	-- { 'theprimeagen/harpoon' }
})

vim.opt.termguicolors = true
vim.cmd.colorscheme('catppuccin-macchiato')
