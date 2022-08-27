class Popup {
    constructor(node, modalName, startDate, endDate) {
        this.node = node;
        this.modalName = modalName ?? 'modal_'+ moment().format('YYYY-MM-DD');
        this.startDate = startDate ?? moment().format('YYYY-MM-DD');
        this.endDate = endDate ?? moment().format('YYYY-MM-DD');
        this.currentData = moment().format('YYYY-MM-DD');
        this.triggers = [];
        this.isShown = false;

        this.mount()
    }

    mount() {
        this.subscribePopupTriggers()
        this.checkShouldPopupBeShown()
        window.addEventListener('beforeunload', ()=>this.unmount())
    }

    unmount() {
        this.triggers.forEach(trigger => {
            trigger.removeEventListener('click', ()=>{
                this.setShow(false)
            })
        })
    }

    subscribePopupTriggers() {
        const triggers = Array.from(this.node.querySelectorAll('.popup-close-trigger'))
        this.triggers = triggers
        triggers.forEach(trigger => {
            trigger.addEventListener('click', ()=>{
                this.setShow(false)
            })
        })
    }

    //    methods
    setLocalStorage(data) {
        return localStorage.setItem('luckyModal', JSON.stringify(data));
    }

    validateIsInPeriod() {
        return moment().isSameOrAfter(this.startDate, 'day')
            && moment().isSameOrBefore(this.endDate, 'day')
    }

    returnModal() {
        let luckyModal = localStorage.luckyModal && JSON.parse(localStorage.luckyModal) || {};
        const modal = luckyModal && luckyModal[this.modalName];

        return [luckyModal, modal]
    }

    checkShouldPopupBeShown() {
        if (!this.validateIsInPeriod()) return false;

        let [luckyModal, modal] = this.returnModal()

        if (!modal || modal.lastShown !== this.currentData) {
            const modalObject = {
                lastShown: this.currentData,
                isNoMoreShow: true
            }
            luckyModal[this.modalName] = modalObject
            this.setLocalStorage(luckyModal)
            this.setShow(true)
        }
    }

    setShow(status) {
        this.isShown = status

        if (status) {
            this.node.classList.add('shown')
            return
        }
        this.node.classList.remove('shown')
    }
}