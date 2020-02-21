import random, itertools
import numpy as np

#import this way to avoid python rocket icon showing up
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def plot_confusion_matrix(full_path, cm, classes, title='Confusion Matrix', cmap=plt.cm.binary, dpi=300):
    """
    This method makes the plot of the confusion matrix.
    :param file_name: The file name of the image
    :param cm: The confusion matrix
    :param classes: The classes
    :param title: The title of the matrix
    :param cmap: The cmap style
    :return:
    """

    fig = plt.figure(random.randint(0,1000000))
    ax = fig.add_subplot(111)

    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.set_title(title)
    fig.colorbar(im)
    tick_marks = np.arange(len(classes))

    ax.grid(False)

    ax.set_xticks(tick_marks)
    ax.set_xticklabels(classes)
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(j, i, cm[i, j], size=13,
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    #plt.tight_layout()
    ax.set_ylabel('True Class')
    ax.set_xlabel('Predicted Class')
    fig.savefig(full_path, format="png", dpi=dpi)
    plt.close(fig)


def plot_thresholds_scores(full_path, thresholds, scores, dpi=300):
    fig = plt.figure(random.randint(0,1000000))
    ax = fig.add_subplot(111)
    ax.plot(thresholds, scores[:, 0], label='$Recall$')
    ax.plot(thresholds, scores[:, 1], label='$Precision$')
    ax.plot(thresholds, scores[:, 2], label='$F_1-Score$')
    ax.plot(thresholds, scores[:, 3], label='$Accuracy$')
    ax.set_ylabel('Score')
    ax.set_xlabel('Threshold')
    ax.legend(loc='best')
    fig.savefig(full_path, format="png", dpi=300)
    plt.close(fig)
