// This code replaces the default sphinx gallery download buttons
// with the 3 download buttons at the top of the page

var downloadNote = $(".sphx-glr-download-link-note.admonition.note");
if (downloadNote.length >= 1) {
    var tutorialUrlArray = $("#tutorial-type").text().split('/');
        tutorialUrlArray[0] = tutorialUrlArray[0] + "_source"

    var githubLink = "https://github.com/pytorch/tutorials/blob/master/" + tutorialUrlArray.join("/") + ".py",
        notebookLink = $(".reference.download")[1].href,
        notebookDownloadPath = notebookLink.split('_downloads')[1],
        colabLink = "https://colab.research.google.com/github/pytorch/tutorials/blob/gh-pages/_downloads" + notebookDownloadPath;

    // Only add the links if they don't already exist
    if ($("#google-colab-link").parent().prop("tagName") !== "A") {
        $("#google-colab-link").wrap("<a href=" + colabLink + " data-behavior='call-to-action-event' data-response='Run in Google Colab' target='_blank'/>");
        $("#download-notebook-link").wrap("<a href=" + notebookLink + " data-behavior='call-to-action-event' data-response='Download Notebook'/>");
        $("#github-view-link").wrap("<a href=" + githubLink + " data-behavior='call-to-action-event' data-response='View on Github' target='_blank'/>");
    }

    // Show the buttons
    $(".pytorch-call-to-action-links").show();
} else {
    // Hide the buttons if not a sphinx-gallery page
    $(".pytorch-call-to-action-links").hide();
}
