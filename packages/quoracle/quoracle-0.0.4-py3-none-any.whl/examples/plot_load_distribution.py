from quoracle import *
import argparse
import matplotlib
import matplotlib.pyplot as plt
import os.path


def main(output_directory: str):
    a = Node('a', capacity=100)
    b = Node('b', capacity=200)
    c = Node('c', capacity=100)
    d = Node('d', capacity=200)
    e = Node('e', capacity=100)
    nodes = [a, b, c, d, e]

    quorum_systems = {
        'majority': QuorumSystem(reads=majority([a, b, c, d, e])),
        'crumbling_walls': QuorumSystem(reads=a*b + c*d*e),
        'paths': QuorumSystem(reads=a*b + a*c*e + d*e + d*c*b),
    }

    for name, qs in quorum_systems.items():
        dist = {0.0: 1., 0.1: 1., 0.2: 1., 0.3: 1., 0.4: 1., 0.5: 1.,
                0.6: 1., 0.7: 1., 0.8: 1., 0.9: 1., 1.0: 1.}
        fig, axes = plt.subplots(3, 4, figsize=(6 * 2, 4 * 2), sharey='all')
        axes_iter = (axes[row][col] for row in range(3) for col in range(4))

        for fr in dist.keys():
            sigma = qs.strategy(read_fraction=fr)
            ax = next(axes_iter)
            plot_load_distribution_on(ax, sigma, nodes)
            ax.set_title(f'Optimized For\nRead Fraction = {fr}')
            ax.set_xlabel('Read Fraction')
            ax.grid()

        sigma = qs.strategy(read_fraction=dist)
        ax = next(axes_iter)
        plot_load_distribution_on(ax, sigma, nodes)
        ax.set_title('Optimized For\nUniform Read Fraction')
        ax.set_xlabel('Read Fraction')
        ax.grid()

        axes[0][0].set_ylabel('Load')
        axes[1][0].set_ylabel('Load')
        axes[2][0].set_ylabel('Load')
        fig.tight_layout()
        output_filename = os.path.join(output_directory, f'{name}.pdf')
        fig.savefig(output_filename)
        print(f'Wrote figure to "{output_filename}".')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',
                        type=str,
                        default='.',
                        help='Output directory')
    args = parser.parse_args()
    main(args.output)
