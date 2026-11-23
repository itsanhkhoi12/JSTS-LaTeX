# ==============================================================================
# LATEXMK CONFIGURATION
# ==============================================================================
use Cwd;

# Prepend project local scripts/bin to PATH if present (provides fallback shims)
my $cwd = Cwd::getcwd();
if ($^O ne 'MSWin32' && -d "$cwd/scripts/bin") {
    $ENV{'PATH'} = "$cwd/scripts/bin:" . $ENV{'PATH'};
}

# Use XeLaTeX engine
$pdf_mode = 5;
$xelatex = 'xelatex -synctex=1 -interaction=nonstopmode -shell-escape %O %S';

# Direct all auxiliary and output files to build/
$out_dir = 'build';
$aux_dir = 'build';

# BibTeX configuration
$bibtex = 'bibtex %O %B';

# Clean file extensions
$clean_ext = 'bbl bcf fdb_latexmk fls lof lot nav out pyg run.xml snm synctex.gz toc vrb xdv %R.synctex(busy) %R.synctex.gz(busy)';
