""" HW2.py

    a cryptanalytic toolkit in Python to analyze the statistical properties of files

    Usage: cipher.py COMMAND [OPTIONS] [ARGS]...

    Commands:
        dist     Calculate frequency distributions of symbols...


    Help for each command is avaible:
        HW2.py COMMAND -h


    Example usage:


      Trigram distribution printed to console ( STDOUT indicated by '-' )

    Qingchen Meng
"""
import click



class Distribution(object):
    """ Base class for analysis routines for symbol distributions.
        Results are dictionary objects with human readable keys.
    """
    def to_readable(self):
        """ Convert dictionary of symbols to readable text """
        pp = []
        for nary in self.result:
            pp.append( "{}: {}\n".format( nary, self.result[nary]))
        return ''.join(pp)


class Ngraph(Distribution):
    """ Looking 'n' symbols at a time, create a dictionary
        of the occurrences of the n-ary string of symbols.
        Default is n=1, a monograph.
    """
    def __init__(self, n=1 ):
        self.n = n

    def analyze(self, text):
        n = self.n
        self.result = {} # results are stored as a dictionary
        for i in range( len(text) - n - 1 ):
            nary = text[ i:i+n ]
            if nary in self.result:
                self.result[nary] += 1
            else:
                self.result[nary] = 1
        return self.result


class Monograph(Distribution):
    def analyze(self, text): self.result = Ngraph( n=1 ).analyze(text)

class Digraph(Distribution):
    def analyze(self, text): self.result = Ngraph( n=2 ).analyze(text)

class Trigraph(Distribution):
    def analyze(self, text): self.result = Ngraph( n=3 ).analyze(text)


# -- additional CLI for HW2
# collect all distribution routines for cli usage
dist_dict = {'mono':Monograph, 'di':Digraph, 'tri':Trigraph, 'ng':Ngraph}
dist_name_list =[ key for key in dist_dict]

# --- 'click' based command-line interface ------------------------------------
@click.version_option(0.1)

@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.pass_context     # ctx
def cli(ctx):
    """ A tool to encrypt or decrypt a file using simple ciphers. """
    pass

@cli.command()
@click.option('--dtype', '-d', 'dist_name', type=click.Choice( dist_name_list ) )
@click.argument('input_file', type=click.File('rb'))
@click.argument('output_file', type=click.File('wb'))
def Dist(dist_name, input_file, output_file):
    """ Calculate frequency distributions of symbols in files.
    """
    D = dist_dict[dist_name] # instantiate class from dictionary
    dist = D()
    text = input_file.read()

    dist.analyze(text)

    output_file.write( dist.to_readable() )

charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ" # The list of characters to be    encrypted
numchars=len(charset) # number of characters that are in the list for encryption

def caesar_crack(crackme,i,newkey):

    print '[*] CRACKING - key: %d; ciphertext: %s' % (i,crackme)
    crackme=crackme.upper()
    plaintext='' #initialise plaintext as an empty string

    while i <= 26:
        for ch in crackme:   #'for' will check each character in plaintext against charset
            if ch in charset:
                pos=charset.find(ch)    #finds the position of the current character
                pos=pos-newkey
            else:
                new='' # do nothing with characters not in charet
            if pos>=len(charset):   #if the pos of the character is more or equal to the charset e.g -22 it will add 26 to get the correct letter positioning/value
                pos=pos+26
            else:
                new=charset[pos]
            plaintext=plaintext+new
        print '[*] plaintext: ' + plaintext

        if i <= 27:
                newkey=newkey+1
                i=i+1
        return plaintext

def main():
    # test cases
    newkey=0
    i=0
    crackme = 'PBATENGHYNGVBAFLBHUNIRPENPXRQGURPBQRNAQGURFUVSGJNFGUVEGRRA'
    # call functions with text cases
    caesar_crack(crackme,i,newkey)

# boilerplate

if __name__ == '__main__':
    cli()
    main()