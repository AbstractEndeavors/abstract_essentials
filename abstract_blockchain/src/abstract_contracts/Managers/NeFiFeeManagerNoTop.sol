//SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;
abstract NeFiUpdateManager is Context{
	function getTreasury() external virtual; returns(address);
	function getBoostManager() external virtual; returns(address);
	function getDropManager() external virtual; returns(address);
	function getProtoManager() external virtual; returns(address);
	function getFeeManager() external virtual; returns(address);
	function getOverseer() external virtual; returns(address);
	function getTeamPool() external virtual; returns(address);
	function getRewardsPool() external virtual; returns(address);
}
abstract contract boostManager is Context {
	function getIncreasedDecay(address _account,uint256 _x) external virtual returns(uint256);
}
abstract contract overseer is Context {
	 function getFee() external virtual view returns(uint256);
}
abstract contract protoManager is Context {
    function collapseProto(address _account, uint256 _x) virtual external ;
    function getDeadStarsData(address _account, uint256 _x) external  virtual returns(string memory,uint256,uint256,uint256,uint256,uint256,uint256,bool,bool);
    function protoAccountData(address _account, uint256 _x) external virtual returns(string memory,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256);
    function protoAccountExists(address _account) external virtual returns (bool);
    function getCollapseDate(address _account,uint256 _x) external virtual view returns(uint256);
    function getdeadStarsLength(address _account) external virtual view returns(uint256);
    function getProtoAccountsLength() external virtual view returns(uint256);
    function getProtoAddress(uint256 _x) external virtual view returns(address);
    function getProtoStarsLength(address _account) external virtual view returns(uint256);
}
contract NeFiFeeManagerNoTop is Ownable{
	using SafeMath for uint256;
	struct TOTALFEES{
		uint256 totalPayable;
		uint256 protos;
		uint256 feesOwed;
		uint256 futureFees;
		uint256 feesPaid;
		uint256 collapsed;
		uint256 feeFroze;
		uint256 insolvent;
		uint256 imploded;
		}
	struct PROTOOWNERS{
		string name;
		uint256 protoCreationDate;
		uint256 protoElapsed;
		uint256 protoCollapseDate;
		uint256 protoNextDue;
		uint256 protoDueElapsed;
		uint256 protoFeesPaid;
		uint256 protoFutureFees;
		uint256 protoIncreasedDecay;
		uint256 protoFeeFroze;
		uint256 protoTotalPayable;
		}
	struct BOOL{
		bool owed;
		bool boolInsolvent;
		bool boolImploded;
		bool boolCollapsed;
		}
	mapping(address => TOTALFEES) public totalfees;
	mapping(address => PROTOOWNERS[]) public protoowners;
	mapping(address => BOOL[]) public bools;
	address[] public protoOwners;
	uint256 teamPerc;
	uint256 rewardsPerc;
	uint256 treasuryPerc;
	uint256 public gracePeriod = 5 days;
	uint256 public protoLife = 500 days;
	uint256 public maxFeePayment = 365 days;
	uint256 public maxPayPeriods = 12;
	uint256 public feePeriod = 31 days;
	bool  boostem = false;
	bool public feeFroze = true;
        address public _protoManager;
        address public _dropManager;
        address public _boostManager;
        address public _overseer;
        address public _updateManager;
        address payable treasury;
        address public NeFiToken;
        address public feeToken;
        address payable rewardsPool;
        address payable teamPool;
	uint256  Zero =0;
	uint256  One = 1;
	address public Guard;
        overseer public over;
        boostManager public boostMGR;
        dropManager public dropMGR;
        NeFiUpdateManager public updateMGR;
	modifier onlyGuard() {require(Guard == _msgSender() || _msgSender() == owner() || _msgSender() == _protoManager || _msgSender() == _dropManager || || _msgSender() == _updateManager, "feeMGR_NOT_GUARD");_;}
	constructor(address updatemanager) {
	    	_updateManager = updatemanager;
	    	updateMGR = updateManager(_updateManager);
	}
//PercentageSplits-----------------------------------------------------------------------------------------------------------------------------
	function payFeeAvax(address _account,uint256 _intervals, uint256 _x) payable external onlyGuard() {
	    uint256 _amount = msg.value;
	    payable(teamPool).transfer(NeFiLib.sendPercentage(_amount,teamPerc));
	    payable(rewardsPool).transfer(NeFiLib.sendPercentage(_amount,rewardsPerc));
	    payable(treasury).transfer(NeFiLib.sendPercentage(_amount,treasuryPerc));
	    uint256 balanceRemainder = _amount.sub(NeFiLib.sendPercentage(_amount,treasuryPerc)).sub(NeFiLib.sendPercentage(_amount,rewardsPerc)).sub(NeFiLib.sendPercentage(_amount,teamPerc));
	    if(balanceRemainder>0){
	    	payable(treasury).transfer(balanceRemainder);
	    }
	    updateFeesPaid(_account,_intervals,_x);
	}
	function divyERC(address token, uint256 _amount,address _account, uint256 _intervals, uint256 _x) payable external onlyGuard() {
	    IERC20 Tok = IERC20(token);
	    Tok.transferFrom(_account, teamPool, NeFiLib.sendPercentage(_amount,teamPerc));
	    Tok.transferFrom(_account, rewardsPool, NeFiLib.sendPercentage(_amount,rewardsPerc));
	    Tok.transferFrom(_account, treasury, NeFiLib.sendPercentage(_amount,treasuryPerc));
	    uint256 leftover =  _amount.sub(NeFiLib.sendPercentage(_amount,teamPerc)).sub(NeFiLib.sendPercentage(_amount,rewardsPerc)).sub(NeFiLib.sendPercentage(_amount,treasuryPerc));
	    Tok.transferFrom(_account, treasury, leftover);
	}
//FeeReconciliation-------------------------------------------------------------------------------------
	function MGRrecPayFees(address _account, uint _intervals,uint256 _x)external onlyGuard(){
    		updateFeesPaid(_account,_intervals,_x);
    	}
    	function reconcileFees() external onlyGuard() {
		for(uint i = 0;i<protoOwners.length;i++){
			INTreconcileAccountFees(protoOwners[i]);
		}
	}
	function reconcileAccountFees(address _account) external onlyGuard() {
		INTreconcileAccountFees(_account);
	}
	function INTreconcileAccountFees(address _account) internal{
		for(uint i = 0;i<getProtoOwnersLength(_account);i++){
			INTreconcileFees(_account,i);
		}
		INTqueryBoolOwed(_account);
		INTupdateFutureFees(_account);
		INTupdateTotalPayable(_account);
	}
	function reconcileFees(address _account,uint256 _x) external  onlyGuard() {
		INTreconcileFees(_account,_x);
	}
	function INTreconcileFees(address _account,uint256 _x) internal{
		INTupdateProtoIncreasedDecay(_account,_x);
		INTqueryProtoCollapseDate(_account,_x);
		INTupdateProtoFeeFroze(_account,_x,block.timestamp);
		INTqueryProtoElapsed(_account,_x);
		INTqueryProtoDueElapsed(_account,_x);
	    	INTqueryBoolOwed(_account);
		INTqueryBoolInsolvent(_account,_x);
		INTqueryProtoFutureFees(_account,_x);
		INTqueryProtoTotalPayable(_account,_x);
	}
	function getTotalfees(address _account) external returns(uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256) {
		TOTALFEES storage _totalfees = totalfees[_account];
		return (_totalfees.totalPayable,_totalfees.protos,_totalfees.feesOwed,_totalfees.futureFees,_totalfees.feesPaid,_totalfees.collapsed,_totalfees.feeFroze,_totalfees.insolvent,_totalfees.imploded);
	}
	function findLowest(address _account) internal returns(uint256){
		uint256 now;
	    	uint256 low;
	    	uint256 lowest = INTgetProtoDueElapsed(_account,0);
	    	INTreconcileAccountFees(_account);
	    	for(uint j = 0;j<INTgetProtoownersLength(_account);j++){
	    		now = INTgetProtoDueElapsed(_account,j);
	    		if(now < lowest && bools[_account][j].boolCollapsed != true && bools[_account][j].boolImploded != true){
	    			low = j;
	    			lowest = INTgetProtoDueElapsed(_account,j);
	      		}
	    	}
    		return low;
   	}
//NAMES-------------------------------------------------------------------------------------------------
	function EXTnameExists(address _account, string memory _name) external returns(bool){
    		return nameExists(_account,_name);
    	}
    	function nameExists(address _account, string memory _name) internal returns(bool){
    		PROTOOWNERS[] storage protos = protoowners[_account];
    		for(uint i = 0;i<protos.length;i++) {
    			PROTOOWNERS storage proto = protos[i];
    			if(keccak256(bytes(proto.name)) == keccak256(bytes(_name))){
    				return true;
    			}
    		}
    		return false;
    	}
    	function updateName(address _account,string memory _Oldname,string memory _newName) external onlyGuard(){
		protoowners[_account][findFromName(_account,_Oldname)].name = _newName;
	}
    	function findFromName(address _account, string memory _name) internal view returns(uint256){
    	    	PROTOOWNERS[] storage protos = protoowners[_account];
    	    	for(uint i = 0;i<protos.length;i++) {
    			PROTOOWNERS storage proto = protos[i];
    			if(keccak256(bytes(proto.name)) == keccak256(bytes(_name))){
    				return i;
    			}
    		}
    	}
//NodesUP-------------------------------------------------------------------------------------------------
    	function INTupdateProtos(address _account,bool _bool,uint256 _protos) internal {
		if(_bool==false){
			totalfees[_account].protos -= _protos;
			totalfees[address(this)].protos -= _protos;
		}else{
			totalfees[_account].protos += _protos;
			totalfees[address(this)].protos += _protos;
		}
	}
	function addProto(address _account,string memory _name) external onlyOwner(){
		INTaddProto(_account,_name);
	}
	function INTaddProto(address _account,string memory _name) internal{
		uint256 _time = block.timestamp;
		if(NeFiLib.addressInList(protoOwners,_account) == false){
			protoOwners.push(_account);
		}	
		uint256 _protoFeeFroze = Zero;
		uint256 life = block.timestamp.add(protoLife);
		PROTOOWNERS[] storage _protoowners = protoowners[_account];
		uint256 len = _protoowners.length.add(1);
		_protoowners.push(PROTOOWNERS({
			name:_name,
			protoCreationDate:block.timestamp,
			protoElapsed:Zero,
			protoCollapseDate:life,
			protoNextDue:block.timestamp,
			protoDueElapsed:Zero,
			protoFeesPaid:Zero,
			protoFutureFees:Zero,
			protoIncreasedDecay:Zero,
			protoFeeFroze:Zero,
			protoTotalPayable:maxPayPeriods
		}));	
		BOOL[] storage _bool = bools[_account];
		_bool.push(BOOL({boolInsolvent:false,boolImploded:false,boolCollapsed:false,owed:false}));
		INTupdateProtos(_account,true,One);
		updateFeesPaid(_account,1,len.sub(1));
	}
//NodesDOWN-------------------------------------------------------------------------------------------------
	function collapseProto(address _account,string memory _name) external onlyOwner() {
		require(nameExists(_account,_name)==true,"the proto to be collapsed could not be found");
		INTcollapse(_account,findFromName(_account,_name));
	}
	function INTcollapse(address _account,uint256 _x) internal{
	    	PROTOOWNERS[] storage protos = protoowners[_account];
	    	BOOL[] storage boo = bools[_account];
	    	for(uint i=_x;i<protos.length;i++){
	    		if(i != protos.length-1){
	  			PROTOOWNERS storage proto_bef = protos[i];
	  			PROTOOWNERS storage proto_now = protos[i+1];
	    			BOOL storage bool_bef = boo[i];
				BOOL storage bool_now = boo[i+1];
		    	        proto_bef.name =proto_now.name;
				proto_bef.protoCreationDate = proto_now.protoCreationDate;
				proto_bef.protoElapsed = proto_now.protoElapsed;
				proto_bef.protoCollapseDate = proto_now.protoCollapseDate;
				proto_bef.protoNextDue = proto_now.protoNextDue;
				proto_bef.protoDueElapsed = proto_now.protoDueElapsed;
				proto_bef.protoFutureFees = proto_now.protoFutureFees;
				proto_bef.protoIncreasedDecay = proto_now.protoIncreasedDecay;
				proto_bef.protoFeeFroze = proto_now.protoFeeFroze;
				proto_bef.protoTotalPayable = proto_now.protoTotalPayable;
				bool_bef.owed = bool_now.owed;
				bool_bef.boolInsolvent = bool_now.boolInsolvent;
				bool_bef.boolImploded = bool_now.boolImploded;
				bool_bef.boolCollapsed = bool_now.boolCollapsed;
	    		}
	    	}
	    	protos.pop();
	    	boo.pop();
    	}
//FeesUpdate-------------------------------------------------------------------------------------------------
	function INTupdateTotalPayable(address _account) internal {
		totalfees[address(this)].totalPayable -= totalfees[_account].totalPayable;
		totalfees[_account].totalPayable = Zero;
		for(uint i=0;i<totalfees[_account].protos;i++){
			totalfees[_account].totalPayable += protoowners[_account][i].protoTotalPayable;
			INTqueryProtoTotalPayable(_account,i);
		}
		totalfees[address(this)].totalPayable += totalfees[_account].totalPayable;
	}
	function INTupdateFutureFees(address _account) internal {
		totalfees[address(this)].futureFees -= totalfees[_account].futureFees;
		totalfees[_account].futureFees = Zero;
		for(uint i=0;i<totalfees[_account].protos;i++){
			totalfees[_account].futureFees += protoowners[_account][i].protoFutureFees;
			INTqueryProtoFutureFees(_account,i);
		}
		totalfees[address(this)].futureFees += totalfees[_account].futureFees;
	}
	function INTupdateFeesPaid(address _account,bool _bool,uint256 _x,uint256 _feesPaid) internal {
		if(_bool==true){
			protoowners[_account][_x].protoFeesPaid +=_feesPaid;
			protoowners[_account][_x].protoNextDue += feePeriod.mul(_feesPaid);
			totalfees[_account].feesPaid += _feesPaid;
			totalfees[address(this)].feesPaid += _feesPaid;
		}else{
			protoowners[_account][_x].protoFeesPaid -=_feesPaid;
			protoowners[_account][_x].protoNextDue -= feePeriod.mul(_feesPaid);
			totalfees[_account].feesPaid -= _feesPaid;
			totalfees[address(this)].feesPaid -= _feesPaid;
		}
	}
	function INTupdateProtoNextDue(address _account,uint256 _x,uint256 _protoNextDue,bool _bool) internal {
		if(_bool == false){
			protoowners[_account][_x].protoNextDue -= _protoNextDue;
		}else{
			protoowners[_account][_x].protoNextDue += _protoNextDue;
		}
		INTqueryBoolInsolvent(_account,_x);
		INTqueryBoolOwed(_account);
		INTqueryProtoFutureFees(_account,_x);
		INTqueryProtoTotalPayable(_account,_x);
	}
//FeesQuery-------------------------------------------------------------------------------------------------
	function INTqueryProtoFutureFees(address _account,uint256 _x) internal {
		protoowners[_account][_x].protoFutureFees = NeFiLib.getMultiple(feePeriod,INTgetProtoDueElapsed(_account,_x));
	}
	function INTqueryProtoTotalPayable(address _account,uint256 _x) internal {
		protoowners[_account][_x].protoTotalPayable = NeFiLib.getMultiple(feePeriod,NeFiLib.getLower(INTgetProtoCollapseDate(_account,_x).sub(block.timestamp),maxFeePayment)).sub(protoowners[_account][_x].protoFutureFees);
	}
    	function updateFeesPaid(address _account,uint _intervals,uint256 _x) internal{
    		if(_x == 101){
	    		for(uint i=0;i<_intervals;i++){
		    		INTupdateFeesPaid(_account,true,findLowest(_account),1);
		    	}
		}else{
			for(uint i=0;i<_intervals;i++){
			
				INTupdateFeesPaid(_account,true,_x,1);
			}
		}
		INTreconcileAccountFees(_account);
    	}
//TimeUpdates-------------------------------------------------------------------------------------------------
	function INTupdateProtoIncreasedDecay(address _account,uint256 _x) internal {
		if(boostem == true){
			protoowners[_account][_x].protoIncreasedDecay = boostMGR.getIncreasedDecay(_account,_x);
		}else{
			protoowners[_account][_x].protoIncreasedDecay = Zero;
		}
	}
	function INTupdateProtoFeeFroze(address _account,uint256 _x,uint256 _time) internal {
		if(feeFroze == false && INTgetFeeFroze() != Zero){
			protoowners[_account][_x].protoFeeFroze =_time.sub(NeFiLib.getHigher(INTgetFeeFroze(),INTgetProtoCreationDate(_account,_x)));
			INTupdateProtoNextDue(_account,_x,protoowners[_account][_x].protoFeeFroze,true);
			totalfees[_account].feeFroze += _time.sub(INTgetFeeFroze());
			protoowners[_account][_x].protoFeeFroze = Zero;
		}else if(feeFroze == true){
			protoowners[_account][_x].protoFeeFroze =_time.sub(NeFiLib.getHigher(INTgetFeeFroze(),INTgetProtoCreationDate(_account,_x)));
			}
	}
	function INTupdateFeeFroze(uint256 _time) internal {
		if(feeFroze == false){
			totalfees[address(this)].feeFroze = Zero;
		}else{
			totalfees[address(this)].feeFroze = _time;
		}
	}
//TimeQuery-------------------------------------------------------------------------------------------------
	function INTqueryProtoElapsed(address _account,uint256 _x) internal{	
		protoowners[_account][_x].protoElapsed = (block.timestamp.sub(INTgetProtoCreationDate(_account,_x))).add(INTgetProtoIncreasedDecay(_account,_x));
	}
	function INTqueryProtoDueElapsed(address _account,uint256 _x) internal{
		uint256 next =  INTgetProtoFeeFroze(_account,_x).add(INTgetProtoNextDue(_account,_x));
		if(NeFiLib.isLower(next,block.timestamp)==true){
			protoowners[_account][_x].protoDueElapsed == 0;
			if(block.timestamp.sub(next)>=gracePeriod){
				INTupdateBoolImploded(_account,_x);
			}
		}
		protoowners[_account][_x].protoDueElapsed = next.sub(block.timestamp);
	}
	function INTqueryProtoCollapseDate(address _account,uint256 _x) internal {
		protoowners[_account][_x].protoCollapseDate = INTgetProtoCreationDate(_account,_x).add(protoLife.add(INTgetProtoIncreasedDecay(_account,_x)));
		if(protoowners[_account][_x].protoCollapseDate <= block.timestamp){
			INTupdateBoolCollapsed(_account,_x);
		}
	}
//BOOLSUpdate------------------------------------------------------------------------------------------------
	function INTupdateBoolImploded(address _account,uint256 _x) internal {
		if(bools[_account][_x].boolImploded != true){
			bools[_account][_x].boolImploded = true;
			totalfees[_account].insolvent += 1;
			totalfees[address(this)].insolvent += 1;
			INTupdateProtos(_account,false,1);
			protoMGR.collapseProto(_account,_x);
		}
	}
	function INTupdateBoolCollapsed(address _account,uint256 _x) internal {
		if(bools[_account][_x].boolCollapsed != true){
			bools[_account][_x].boolCollapsed = true;
			totalfees[_account].collapsed += 1;
			totalfees[address(this)].collapsed += 1;
			INTupdateProtos(_account,false,1);
			protoMGR.collapseProto(_account,_x);
		}
	}
//BOOLSQuery-------------------------------------------------------------------------------------------------
	function INTqueryBoolOwed(address _account) internal {
		totalfees[address(this)].feesOwed -= totalfees[_account].feesOwed;
		totalfees[_account].feesOwed = Zero;
		for(uint i=0;i<totalfees[_account].protos;i++){
			if(INTgetProtoDueElapsed(_account,i)<feePeriod){
	    			bools[_account][i].owed = true;
	    			totalfees[_account].feesOwed += 1;
	    			INTqueryBoolInsolvent(_account,i);
	    		}else{
	    			bools[_account][i].owed = false;
	    		}
		}
		totalfees[address(this)].feesOwed += totalfees[_account].feesOwed;
	}
	function INTqueryBoolInsolvent(address _account,uint256 _x) internal {
		if(INTgetProtoDueElapsed(_account,_x)>0){
			bools[_account][_x].boolInsolvent = false;
		}else if(INTgetProtoDueElapsed(_account,_x)==0){
			bools[_account][_x].boolInsolvent = true;
		}
	}
//internal gets---------------------------------------------------------------------------------------------------------
	function INTgetBoolImploded(address _account,uint256 _x) internal view returns(bool){
		return bools[_account][_x].boolImploded;
	}
	function INTgetInsolvent(address _account) internal view returns(uint256){
		return totalfees[_account].insolvent;
	}
	function INTgetName(address _account,uint256 _x) internal view returns(string memory){
		return protoowners[_account][_x].name;
	}
	function INTgetTotalPayable(address _account) internal view returns(uint256){
		return totalfees[_account].totalPayable;
	}
	function INTgetFeeFroze() internal view returns(uint256){
		return totalfees[address(this)].feeFroze;
	}
	function INTgetProtoDueElapsed(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoDueElapsed;
	}
	function INTgetFeesOwed(address _account) internal view returns(uint256){
		return totalfees[_account].feesOwed;
	}
	function INTgetProtoElapsed(address _account,uint256 _x) internal view returns (uint256){
		return protoowners[_account][_x].protoElapsed;
	}
	function INTgetBoolOwed(address _account,uint256 _x) internal view returns(bool){
		return bools[_account][_x].owed;
	}
	function INTgetBoolInsolvent(address _account,uint256 _x) internal view returns(bool){
		return bools[_account][_x].boolInsolvent;
	}
	function INTgetProtos(address _account) internal view returns(uint256){
		return totalfees[_account].protos;
	}
	function INTgetFutureFees(address _account) internal view returns(uint256){
		return totalfees[_account].futureFees;
	}
	function INTgetFeesPaid(address _account) internal view returns(uint256){
		return totalfees[_account].feesPaid;
	}
	function INTgetProtoCreationDate(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoCreationDate;
	}
	function INTgetProtoNextDue(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoNextDue;
	}
	function INTgetProtoFutureFees(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoFutureFees;
	}
	function INTgetProtoIncreasedDecay(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoIncreasedDecay;
	}
	function INTgetProtoCollapseDate(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoCollapseDate;
	}
	function INTgetProtoFeeFroze(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoFeeFroze;
	}
	function INTgetProtoTotalPayable(address _account,uint256 _x) internal view returns(uint256){
		return protoowners[_account][_x].protoTotalPayable;
	}
	function INTgetBoolCollapsed(address _account,uint256 _x) internal view returns(bool){
		return bools[_account][_x].boolCollapsed;
	}
	function INTgetImploded(address _account) internal view returns(uint256){
		return totalfees[_account].imploded;
	}
	function INTgetCollapsed(address _account) internal view returns(uint256){
		return totalfees[_account].collapsed;
	}
	function updateBoolOwed(address _account,uint256 _x,bool _owed) external onlyOwner() {
		bools[_account][_x].owed = _owed;
	}
	function updateTotalPayable(address _account,uint256 _totalPayable) external  onlyOwner() {
		totalfees[_account].totalPayable = _totalPayable;
	}
	function updateProtos(address _account,uint256 _protos) external  onlyOwner() {
		totalfees[_account].protos = _protos;
	}
	function updateFeesOwed(address _account,uint256 _feesOwed) external  onlyOwner() {
		totalfees[_account].feesOwed = _feesOwed;
	}
	function updateFutureFees(address _account,uint256 _futureFees) external  onlyOwner() {
		totalfees[_account].futureFees = _futureFees;
	}
	function updateCollapsed(address _account,uint256 _collapsed) external  onlyOwner() {
		totalfees[_account].collapsed = _collapsed;
	}
	function updateFeeFroze(address _account,uint256 _feeFroze) external  onlyOwner() {
		totalfees[_account].feeFroze = _feeFroze;
	}
	function updateInsolvent(address _account,uint256 _insolvent) external  onlyOwner() {
		totalfees[_account].insolvent = _insolvent;
	}
	function updateImploded(address _account,uint256 _imploded) external  onlyOwner() {
		totalfees[_account].imploded = _imploded;
	}
	function updateName(address _account,uint256 _x,string memory _name) external  onlyOwner() {
		protoowners[_account][_x].name = _name;
	}
	function updateProtoCreationDate(address _account,uint256 _x,uint256 _protoCreationDate) external  onlyOwner() {
		protoowners[_account][_x].protoCreationDate = _protoCreationDate;
	}
	function updateProtoCollapseDate(address _account,uint256 _x,uint256 _protoCollapseDate) external  onlyOwner() {
		protoowners[_account][_x].protoCollapseDate = _protoCollapseDate;
	}
	function updateProtoNextDue(address _account,uint256 _x,uint256 _protoNextDue) external  onlyOwner() {
		protoowners[_account][_x].protoNextDue = _protoNextDue;
	}
	function updateBoolCollapsed(address _account,uint256 _x,bool _bool) external  onlyOwner() {
		bools[_account][_x].boolCollapsed = _bool;
	}
	function updateProtoFutureFees(address _account,uint256 _x,uint256 _protoFutureFees) external  onlyOwner() {
		protoowners[_account][_x].protoFutureFees = _protoFutureFees;
	}
	function updateProtoIncreasedDecay(address _account,uint256 _x,uint256 _protoIncreasedDecay) external  onlyOwner() {
		protoowners[_account][_x].protoIncreasedDecay = _protoIncreasedDecay;
	}
	function updateProtoFeeFroze(address _account,uint256 _x,uint256 _protoFeeFroze) external  onlyOwner() {
		protoowners[_account][_x].protoFeeFroze = _protoFeeFroze;
	}
	function updateBoolImploded(address _account,uint256 _x,bool _boolImploded) external  onlyOwner() {
		bools[_account][_x].boolImploded = _boolImploded;
	}
	function updateProtoTotalPayable(address _account,uint256 _x,uint256 _protoTotalPayable) external onlyOwner() {
		protoowners[_account][_x].protoTotalPayable = _protoTotalPayable;
	}
//externalGets------------------------------------------------------------------------------------------------------------
	function getProtoOwnersLength(address _account) internal returns(uint256){
    		PROTOOWNERS[] storage protos = protoowners[_account];
		return protos.length;
	}
	function getTotalPayable(address _account) external view returns(uint256){
		return totalfees[_account].totalPayable;
	}
	function getProtos(address _account) external view returns(uint256){
		return totalfees[_account].protos;
	}
	function getFeesOwed(address _account) external view returns(uint256){
		return totalfees[_account].feesOwed;
	}
	function getFutureFees(address _account) external view returns(uint256){
		return totalfees[_account].futureFees;
	}
	function getFeesPaid(address _account) external view returns(uint256){
		return totalfees[_account].feesPaid;
	}
	function getInsolvent(address _account) external view returns(uint256){
		return totalfees[_account].insolvent;
	}
	function getFeeFroze(address _account) external view returns(uint256){
		return totalfees[_account].feeFroze;
	}
	function getName(address _account,uint256 _x) external view returns(string memory){
		return protoowners[_account][_x].name;
	}
	function getProtoCreationDate(address _account,uint256 _x) external view returns(uint256){
		return protoowners[_account][_x].protoCreationDate;
	}
	function getProtoCollapseDate(address _account,uint256 _x) external view returns(uint256){
		return protoowners[_account][_x].protoCollapseDate;
	}
	function getProtoNextDue(address _account,uint256 _x) external view returns(uint256){
		return protoowners[_account][_x].protoNextDue;
	}
	function getProtoIncreasedDecay(address _account,uint256 _x) external view returns(uint256){
		return protoowners[_account][_x].protoIncreasedDecay;
	}
	function getProtoFutureFees(address _account,uint256 _x) external view returns(uint256){
		return protoowners[_account][_x].protoFutureFees;
	}
	function getProtoFeeFroze(address _account,uint256 _x) external view returns(uint256){
		return protoowners[_account][_x].protoFeeFroze;
	}
	function getProtoTotalPayable(address _account,uint256 _x) external view returns(uint256){
		return protoowners[_account][_x].protoTotalPayable;
	}
	function getBoolInsolvent(address _account,uint256 _x) external view returns(bool){
		return bools[_account][_x].boolInsolvent;
	}
	function getBoolImploded(address _account,uint256 _x) external view returns(bool){
		return bools[_account][_x].boolImploded;
	}
	function getBoolCollapsed(address _account,uint256 _x) external view returns(bool){
		return bools[_account][_x].boolCollapsed;
	}
//getStruct--------------------------------------------------------------------------------------------------------------------------------------
	function getTotalfees(address _account,uint256 _x) external returns(uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256){
		TOTALFEES storage _totalfees = totalfees[_account];
		return (_totalfees.totalPayable,_totalfees.protos,_totalfees.feesOwed,_totalfees.futureFees,_totalfees.feesPaid,_totalfees.collapsed,_totalfees.feeFroze,_totalfees.insolvent,_totalfees.imploded);
	}
	function getProtoowners(address _account,uint256 _x) external returns(string memory,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256){
		PROTOOWNERS[] storage _protoowners = protoowners[_account];
		PROTOOWNERS storage _protoowners_ = _protoowners[_x];
		return (_protoowners_.name,_protoowners_.protoCreationDate,_protoowners_.protoElapsed,_protoowners_.protoCollapseDate,_protoowners_.protoNextDue,_protoowners_.protoDueElapsed,_protoowners_.protoFutureFees,_protoowners_.protoIncreasedDecay,_protoowners_.protoFeeFroze,_protoowners_.protoTotalPayable);
	}
	function getProtoownersAccountsLength() external returns(uint256){
		return protoOwners.length;
	}
	function getProtoAddress(uint256 _x) external returns(address){
		return protoOwners[_x];
	}
	function getBool(address _account,uint256 _x) external returns(bool,bool,bool,bool){
		BOOL[] storage _bool = bools[_account];
		BOOL storage _bool_ = _bool[_x];
		return (_bool_.owed,_bool_.boolInsolvent,_bool_.boolImploded,_bool_.boolCollapsed);
	}
	function getProtoownersLength(address _account) external view returns(uint256){
		return INTgetProtoownersLength(_account);
	}
	function INTgetProtoownersLength(address _account) internal view returns(uint256){
		PROTOOWNERS[] storage _protoowners = protoowners[_account];
		 return _protoowners.length;
	}
//onlyOwnerFunctions----------------------------------------------------------------------------------------------------------------------------------
	function pauseFees(bool _x) external onlyOwner {
	    	feeFroze = _x;
		uint256 _time = block.timestamp;
		for(uint j = 0;j<protoOwners.length;j++){
			address _account = protoOwners[j];
			for(uint i = 0;i<INTgetProtoownersLength(_account);i++) {
		    		INTupdateProtoFeeFroze(_account,i,_time);
		    	}
		}
		INTupdateFeeFroze(_time);
	}
    	function changeMaxPeriods(uint256 _periods) external  onlyOwner() {
    		maxPayPeriods = _periods;
    		maxFeePayment = maxPayPeriods.mul(feePeriod);
   	 }
    	function changeFeePeriod(uint256 _days) external onlyOwner() {
    		uint256 maxPeriods = NeFiLib.getMultiple(feePeriod,maxFeePayment);
    		feePeriod = _days.mul(1 days);
    		maxFeePayment = maxPeriods.mul(feePeriod);
        }
        function boostit(bool _bool) external onlyOwner(){
        	boostem = _bool;
        }
        function updateRewards_team_treasuryPercentage(uint256[] memory  _perc) external onlyOwner(){
        	rewardsPerc =_perc[0];
        	teamPerc =_perc[1];
        	treasuryPerc =_perc[2];
        }
//changeWallets-----------------------------------------------------------------------------------------------
    function updateNeFiToken(address _account) external onlyGuard(){
    	INTupdateNeFiToken(_account);
    }
    function INTupdateNeFiToken(address _account) internal{
    	NeFiToken = _account;
    	NeFiTok = IERC20(NeFiToken);
    }
    function updateFeeToken(address _account) external onlyGuard(){
    	INTupdateFeeToken(_account);
    }
    function INTupdateFeeToken(address _account) internal{
    	feeToken = _account;
    	feeTok = IERC20(feeToken);
    }
    function updateOverseer(address _account) external onlyGuard(){
    	INTupdateOverseer(_account);
    }
    function INTupdateOverseer(address _account) internal{
    	_overseer = _account;
    	over = overseer(_overseer);
    }
    function updateDropManager(address _account) external onlyGuard(){
    	INTupdateDropManager(_account);
    }
    function INTupdateDropManager(address _account) internal{
    	_dropManager = _account;
    	dropMGR = dropManager(_dropManager);
    }
    function updateprotoManager(address _account) external onlyGuard(){
    	INTupdateprotoManager(_account);
    }
    function INTupdateprotoManager(address _account) internal{
    	_protoManager = _account;
    	protoMGR = protoManager(_protoManager);
    }
    function updateBoostManager(address _account) external onlyGuard(){
    	INTupdateBoostManager(address _account);
    }
    function INTupdateBoostManager(address _account) internal{
    	_boostManager = _account;
    	boostMGR = boostManager(_boostManager);
    }
    function updateTreasury(address payable _account) external onlyGuard(){
    	INTupdateTreasury(_account);
    }
    function INTupdateTreasury(address payable _account) internal{
    	treasury = _account;
    }
    function updateTeamPool(address _account) external onlyGuard(){
    	INTupdateTeamPool(_account);
    }
    function INTupdateTeamPool(address _account) internal{
        	teamPool = _account;
        }
    function updateRewardsPool(address _account) external onlyGuard(){
    	INTupdateRewardsPool(_account);
    }
    function INTupdateRewardsPool(address _account) internal{
        	rewardsPool = _account;
        }
    function updateGuard(address newVal) external onlyOwner(){
        Guard = newVal; //token swap address
    }
    function updateManagers(address newVal) external onlyOwner() {
    	if(NeFiLib.addressInList(Managers,newVal) ==false){
        	Managers.push(newVal); //token swap address
        }
    }
//Overflow-----------------------------------------------------------------------------------------
    function transferOut(address payable _to,uint256 _amount) payable external  onlyOwner(){
		_to.transfer(_amount);
	}
    function transferAllOut(address payable _to,uint256 _amount) payable external onlyOwner(){
		_to.transfer(address(this).balance);
	}
    function sendAllTokenOut(address payable _to,address _token) external onlyOwner(){
		IERC20 newtok = IERC20(_token);
		newtok.transferFrom(address(this), _to, newtok.balanceOf(address(this)));
	}
}
