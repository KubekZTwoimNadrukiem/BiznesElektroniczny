<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class Yarn_Assurance extends Module {
public function __construct()
    {
        $this->name = 'yarn_assurance';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'KubekZMoimNadrukiem';
        $this->need_instance = 0;
        $this->ps_versions_compliancy = [
            'min' => '1.7.0.0',
            'max' => '8.99.99',
        ];
        $this->bootstrap = true;

        parent::__construct();

        $this->displayName = $this->trans('Yarnstreet assurance stuff', [], 'Modules.Yarnassurance.Admin');
        $this->description = $this->trans('Phone number, working time, shipping, returns', [], 'Modules.Yarnassurance.Admin');

        $this->confirmUninstall = $this->trans('Are you sure you want to uninstall?', [], 'Modules.Yarnassurance.Admin');

        if (!Configuration::get('YARN_ASSURANCE_NAME')) {
            $this->warning = $this->trans('No name provided', [], 'Modules.Yarnassurance.Admin');
        }
    }

public function install()
{
    if (Shop::isFeatureActive()) {
        Shop::setContext(Shop::CONTEXT_ALL);
    }

   return (
        parent::install()
	&& $this->registerHook('footerBefore')
	&& $this->registerHook('home')
	&& $this->registerHook('reassurrance')
        && Configuration::updateValue('YARN_ASSURANCE_NAME', 'yarn_assurance')
    );
}

public function uninstall()
{
    return (
        parent::uninstall() 
        && Configuration::deleteByName('YARN_ASSURANCE_NAME')
    );
}

public function hookDisplayFooterBefore($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_assurance_name' => Configuration::get('YARN_ASSURANCE_NAME'),
          'yarn_assurance_link' => $this->context->link->getModuleLink('yarn_assurance', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_assurance.tpl');
}

public function hookDisplayHome($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_assurance_name' => Configuration::get('YARN_ASSURANCE_NAME'),
          'yarn_assurance_link' => $this->context->link->getModuleLink('yarn_assurance', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_assurance.tpl');
}

public function hookDisplayReassurance($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_assurance_name' => Configuration::get('YARN_ASSURANCE_NAME'),
          'yarn_assurance_link' => $this->context->link->getModuleLink('yarn_assurance', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_assurance.tpl');
}

public function hookDisplayHeader()
{
  $this->context->controller->addCSS($this->_path.'css/yarn_assurance.css', 'all');
}


}
