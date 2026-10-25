from app import classify, draft_reply

def test_refund_classification():
    assert classify('Where is my refund?') == 'refund'

def test_escalates_urgent_case():
    assert draft_reply('urgent legal issue')['needs_human_review'] is True
